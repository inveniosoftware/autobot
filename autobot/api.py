# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Autobot API."""

import yaml
import copy

from autobot.config_loader import Config
from autobot.github import GitHubAPI

class BotAPI:
    """Bot's API."""

    def __init__(self, config: Config):
        """Bot initialization."""
        self.config = config
        self.report = GitHubAPI(
            self.config["AUTOBOT_OWNER"],
            self.config["AUTOBOT_GH_TOKEN"],
            self.config.repositories
        ).report()

    @classmethod
    def md_report(cls, report):
        """Returns the report in markdown format."""
        md_report = ""
        for repo in report.keys():
            repo_report = report[repo]
            md_report += f"\n### [{repo_report['url'].split('/')[-1]}]({repo_report['url']})\n"
            for (action, targets) in repo_report["actions"].items():
                md_report += f"- **{action}**\n"
                for target in targets:
                    md_report += (
                        f"  - {target['url']}: {target['title']} "
                        f"({target['creation_date'].date()})\n"
                    )
        return md_report

    def formatted_report(self, format):
        """Returns the report in the specified format."""
        if format == "json":
            return self.report
        elif format == "yaml":
            return yaml.dump(self.report)
        elif format == "markdown":
            return self.md_report(self.report)
        return self.report

    def generate_report(self, maintainer: str):
        """Returns the report in markdown format."""
        report = copy.deepcopy(self.report)
        for repo in self.report.keys():
            repo_report = report[repo]
            if maintainer not in repo_report["maintainers"]:
                del report[repo]
        return report

    def send_report(self, maintainer: str, format: str):
        """Send the report to a maintainer (on Gitter or via email)."""
        report = self.generate_report(maintainer=maintainer)
        if format == "json":
            return report
        elif format == "yaml":
            return yaml.dump(report)
        elif format == "markdown":
            return self.md_report(report)
        return report
