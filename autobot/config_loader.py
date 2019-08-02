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

from dotenv.main import dotenv_values

import autobot.config as config


class Config:
    """Interact with configuration variables."""

    dotenv_path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), ".env")

    ini_parser = ConfigParser()
    ini_path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), "config.ini")

    config = {}

    @classmethod
    def __init__(cls, **kwargs):
        """Initialize configuration."""
        cls.load_config(**kwargs)

    @classmethod
    def load_config(cls, **kwargs):
        """Get autobot configuration values."""
        cls.config = cls.env_config()
        cls.ini_parser.optionxform = str
        cls.ini_parser.read(cls.ini_path)
        cls.config.update(cls.ini_config())
        cls.config.update(kwargs)
        py_config = cls.py_config()
        defaults = {
            key: py_config[key] for key in py_config if key not in cls.config.keys()
        }
        cls.config.update(defaults)
        cls.config = {key: cls.config[key] for key in py_config}

    @classmethod
    def env_config(cls):
        """Get autobot configuration values from .env file."""
        return dotenv_values(cls.dotenv_path)

    @classmethod
    def ini_config(cls):
        """Get autobot configuration values from config.ini file."""
        return cls.ini_parser["AUTOBOT"]

    @classmethod
    def py_config(cls):
        """Get autobot configuration values from config.py file."""
        res = {}
        for k in dir(config):
            if k.startswith("AUTOBOT_"):
                res.setdefault(k, getattr(config, k))
        return res
