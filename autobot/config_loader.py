# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Performs project's configuration loading."""

import os
from configparser import ConfigParser

import yaml
from dotenv.main import dotenv_values

import autobot.config as config
from autobot.utils import cached_property


class Config(dict):
    """Interact with configuration variables."""

    dotenv_path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), ".env")

    ini_path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), "config.ini")

    # def __init__(self, dotenv=None, ini=None, defaults=True, *arg, **kw):
    #     """Initialize configuration."""
    #     super(Config, self).__init__()
    #     self.update(self.load(dotenv=dotenv, ini=ini, defaults=defaults, *arg, **kw))

    @classmethod
    def load(cls, dotenv=None, ini=None, defaults=True, *arg, **kw):
        """Load configuration."""
        conf = cls()
        if defaults:
            py_conf = cls.py_config()
            conf.update(py_conf)
        if dotenv:
            dotenv_conf = (
                cls.dotenv_config()
                if isinstance(dotenv, bool)
                else cls.dotenv_config(dotenv)
            )
            conf.update(dotenv_conf)
        if ini:
            ini_conf = (
                cls.ini_config() if isinstance(ini, bool) else cls.ini_config(ini)
            )
            conf.update(ini_conf)
        user_defined_conf = {
            key: val for (key, val) in kw.items() if key in conf.keys()
        }
        conf.update(user_defined_conf)
        return conf

    @classmethod
    def dotenv_config(cls, path=dotenv_path, prefix="AUTOBOT_"):
        """Get autobot configuration values from .env file."""
        return dotenv_values(path)

    @classmethod
    def ini_config(cls, path=ini_path):
        """Get autobot configuration values from config.ini file."""
        ini_parser = ConfigParser()
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
        with open(self["AUTOBOT_INFO_PATH"]) as fp:
            data = yaml.load(fp)
        return data["orgs"][self["AUTOBOT_OWNER"]]

    @cached_property
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
