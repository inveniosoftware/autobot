# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2019 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for `autobot` package."""

import os
import sys


def test_config_content(config):
    """Test configuration content."""
    assert isinstance(config, dict)
    assert isinstance(config["AUTOBOT_GH_TOKEN"], str)
    assert isinstance(config["AUTOBOT_GITTER_TOKEN"], str)
    assert isinstance(config["AUTOBOT_INFO_PATH"], str)
    assert os.path.isfile(
        os.path.join(os.path.dirname(__file__), config["AUTOBOT_INFO_PATH"])
    )
    assert isinstance(config["AUTOBOT_MAINTAINERS"], list)
    for maintainer in config["AUTOBOT_MAINTAINERS"]:
        assert isinstance(maintainer, str)
    assert isinstance(config["AUTOBOT_OWNER"], str)
    assert isinstance(config["AUTOBOT_REPOS"], list)
    for repo in config["AUTOBOT_REPOS"]:
        assert isinstance(repo, str)
