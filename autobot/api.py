# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Autobot API."""

import yaml

from autobot.config_loader import Config
from autobot.github import GitHubAPI

# config = Config(...)
# api = BotAPI(config)
# api.generate_report(maintaine='slint')
# md_report = BotAPI.report2md(report)


class BotAPI:
    """Bot's API."""

    def __init__(self, config: Config):
        """Bot initialization."""
        self.config = config
        self.report = GitHubAPI(
            self.config["AUTOBOT_OWNER"],
            self.config["AUTOBOT_GH_TOKEN"],
            self.config.repositories
        ).report(self.config.repositories())

    def generate_report(self, **kwargs):
        """Rearranges and returns the report."""
        report = []
        maintainer = kwargs.get("maintainer", None)
        for r in self.report[0]["repos"]:
            exclude = ["actions"]
            rreport = {
                "actions": {},
                "repo": {key: val for (key, val) in r.items() if key not in exclude},
            }
            for ra in r["actions"]:
                if "prs" in ra.keys():
                    for pr in ra["prs"]:
                        for pra in pr["actions"]:
                            if "comments" in pra.keys():
                                continue
                            for key in pra.keys():
                                if key not in rreport["actions"].keys():
                                    rreport["actions"][key] = []
                                if (not maintainer) or (maintainer in pra[key]):
                                    rreport["actions"][key].append(
                                        {
                                            "maintainers": pra[key],
                                            "pr": {
                                                key: val
                                                for (key, val) in pr.items()
                                                if key not in exclude
                                            },
                                        }
                                    )
                if "issues" in ra.keys():
                    for issue in ra["issues"]:
                        for ia in issue["actions"]:
                            if "comments" in ia.keys():
                                continue
                            for key in ia.keys():
                                if key not in rreport["actions"].keys():
                                    rreport["actions"][key] = []
                                if (not maintainer) or (maintainer in ia[key]):
                                    rreport["actions"][key].append(
                                        {
                                            "maintainers": ia[key],
                                            "issue": {
                                                key: val
                                                for (key, val) in issue.items()
                                                if key not in exclude
                                            },
                                        }
                                    )
            report.append(rreport)
        return report

    @classmethod
    def md_report(cls, report):
        """Returns the report in markdown format."""
        res = ""
        for rreport in report:
            res += f"### [{rreport['repo']['url'].split('/')[-1]}]({rreport['repo']['url']})\n"
            for (action, targets) in rreport["actions"].items():
                res += f"- {action}\n"
                for target in targets:
                    if "pr" in target.keys():
                        res += (
                            f"  - {target['pr']['url']}: {target['pr']['title']} "
                            f"({target['pr']['creation_date'].date()})\n"
                        )
                    elif "issue" in target.keys():
                        res += (
                            f"  - {target['issue']['url']}: {target['issue']['title']} "
                            f"({target['issue']['creation_date'].date()})\n"
                        )
                    else:
                        continue
        return res

    def formatted_report(self, format):
        """Returns the report in the specified format."""
        res = self.generate_report()
        if format == "json":
            return res
        elif format == "yaml":
            return yaml.dump(res)
        elif format == "markdown":
            return self.md_report(res)
        return res

    def send_report(self, maintainer: str, format: str):
        """Send the report to a maintainer (on Gitter or via email)."""
        res = self.generate_report(maintainer=maintainer)
        if format == "json":
            return res
        elif format == "yaml":
            return yaml.dump(res)
        elif format == "markdown":
            return self.md_report(res)
        return res
