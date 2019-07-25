# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2019 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration options for Autobot."""

import os

import yaml
from dotenv import load_dotenv


class Config:
    """Loads config from environment and files."""

    def __init__(self, **kwargs):
        """Config initialization."""
        load_dotenv()
        self.owner = kwargs.get("owner", os.getenv("OWNER"))
        self.repos = kwargs.get("repos", [])
        self.maintainers = kwargs.get("maintainers", [])
        self.GITHUB_TOKEN = kwargs.get("github_token", os.getenv("GH_TOKEN"))
        self.INFO_PATH = kwargs.get(
            "info_path", os.getenv(self.owner.upper() + "_INFO")
        )
        self.GITTER_TOKEN = "CHANGE_ME"
        self.MAIL_SETTINGS = {...}

    def _load_repositories_yml(self):
        """Load repository.yml file."""
        return yaml.load(open(self.INFO_PATH))["orgs"][self.owner]

    def _load_repositories(self):
        """Load repository.yml file into dictionary with repositories as keys."""
        info = self._load_repositories_yml()
        res = {
            repo: info["repositories"][repo]["maintainers"]
            for repo in info["repositories"].keys()
        }
        if self.repos:
            res = {repo: res[repo] for repo in self.repos}
        if self.maintainers:
            res = {
                repo: list(filter(lambda m: m in res[repo], self.maintainers))
                for repo in res.keys()
            }
        return {r: m for r, m in res.items() if m}

    def _invert_list_dict(self, d):
        """Invert dictionary `d`."""
        keys = list(set([k for val in d.values() for k in val]))
        res = dict.fromkeys(keys)
        for k in res.keys():
            res[k] = [val for (val, l) in d.items() if k in l]
        return res

    def _load_maintainers(self):
        """Load repository.yml file into dictionary with maintainers as keys."""
        info = self._load_repositories()
        return self._invert_list_dict(info)
