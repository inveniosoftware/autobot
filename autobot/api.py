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


class BotAPI:
    """Generates report."""

    @classmethod
    def __init__(cls, config: Config):
        """Bot initialization."""
        cls.config = config.config
        cls.report = GitHubAPI(
            cls.config["AUTOBOT_OWNER"], cls.config["AUTOBOT_GH_TOKEN"]
        ).report(cls.load_repositories())

    @classmethod
    def generate_report(cls, maintainer: str) -> dict:
        """Generates a report for a maintainer."""
        res = cls.report[0]["repos"]
        print(res)
        print(
            "---------------------------------------------------------------------------------"
        )
        return res

    @classmethod
    def send_report(cls, maintainer: str, format: str):
        """Send the report to a maintainer (on Gitter or via email)."""
        res = cls.generate_report(maintainer)
        if format == "markdown":
            """ TO DO """

    @classmethod
    def load_repositories_yml(cls):
        """Load repository.yml file."""
        return yaml.load(open(cls.config["AUTOBOT_INFO_PATH"]))["orgs"][
            cls.config["AUTOBOT_OWNER"]
        ]

    @classmethod
    def load_repositories(cls):
        """Load repository.yml file into dictionary with repositories as keys."""
        info = cls.load_repositories_yml()
        res = {
            repo: info["repositories"][repo]["maintainers"]
            for repo in info["repositories"].keys()
        }
        if cls.config["AUTOBOT_REPOS"]:
            res = {repo: res[repo] for repo in cls.config["AUTOBOT_REPOS"]}
        if cls.config["AUTOBOT_MAINTAINERS"]:
            res = {
                repo: list(
                    filter(lambda m: m in res[repo], cls.config["AUTOBOT_MAINTAINERS"])
                )
                for repo in res.keys()
            }
        return {r: m for r, m in res.items() if m}

    @classmethod
    def invert_list_dict(cls, d):
        """Invert dictionary `d`."""
        keys = list(set([k for val in d.values() for k in val]))
        res = dict.fromkeys(keys)
        for k in res.keys():
            res[k] = [val for (val, l) in d.items() if k in l]
        return res

    @classmethod
    def load_maintainers(cls):
        """Load repository.yml file into dictionary with maintainers as keys."""
        info = cls.load_repositories()
        return cls.invert_list_dict(info)
