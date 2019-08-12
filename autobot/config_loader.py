# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Performs project's configuration loading."""

import os
import yaml
from configparser import ConfigParser

from dotenv.main import dotenv_values

import autobot.config as config


class Config(dict):
    """Interact with configuration variables."""

    def __init__(self, *arg, **kw):
        """Initialize configuration."""
        super(Config, self).__init__(*arg, **kw)

    @classmethod
    def load(cls, env=None, ini=None, defaults=None, *arg, **kw):
        """Load configuration."""
        conf = cls(*arg, **kw)
        if env:
            env_conf = {
                key: val
                for (key, val) in cls.env_config(env).items()
                if key not in conf.keys()
            }
            conf.update(env_conf)
        if ini:
            ini_conf = {
                key: val
                for (key, val) in cls.ini_config(ini).items()
                if key not in conf.keys()
            }
            conf.update(ini_conf)
        if defaults:
            py_conf = {
                key: val
                for (key, val) in cls.py_config().items()
                if key not in conf.keys()
            }
            conf.update(py_conf)
        return conf

    @classmethod
    def env_config(cls, path=None, prefix="AUTOBOT_"):
        """Get autobot configuration values from .env file."""
        if not path:
            path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), ".env")
        return dotenv_values(path)

    @classmethod
    def ini_config(cls, path=None):
        """Get autobot configuration values from config.ini file."""
        ini_parser = ConfigParser()
        if not path:
            path = os.path.join(
                os.path.abspath(os.path.join(__file__, "..")), "config.ini"
            )
        ini_parser.optionxform = str
        ini_parser.read(path)
        return ini_parser["AUTOBOT"]

    @classmethod
    def py_config(cls):
        """Get autobot configuration values from config.py file."""
        py_conf = {}
        for k in dir(config):
            if k.startswith("AUTOBOT_"):
                py_conf.setdefault(k, getattr(config, k))
        return py_conf

    def load_repositories_yml(self):
        """Load repositories.yml file."""
        return yaml.load(open(self["AUTOBOT_INFO_PATH"]))["orgs"][
            self["AUTOBOT_OWNER"]
        ]

    @property
    def repositories(self):
        """Load repositories.yml file into dictionary with repositories as keys."""
        info = self.load_repositories_yml()
        res = {
            repo: info["repositories"][repo]["maintainers"]
            for repo in info["repositories"].keys()
        }
        if self["AUTOBOT_REPOS"]:
            res = {repo: res[repo] for repo in self["AUTOBOT_REPOS"]}
        if self["AUTOBOT_MAINTAINERS"]:
            res = {
                repo: list(
                    filter(lambda m: m in res[repo], self["AUTOBOT_MAINTAINERS"])
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

    @property
    def maintainers(self):
        """Load repository.yml file into dictionary with maintainers as keys."""
        info = self.repositories
        return self.invert_list_dict(info)
