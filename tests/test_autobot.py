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
    assert isinstance(config.owner, str)
    assert isinstance(config.GITHUB_TOKEN, str)
    assert isinstance(config.INFO_PATH, str)
    assert os.path.isfile(os.path.join(os.path.dirname(__file__), config.INFO_PATH))
    assert isinstance(config.repos, list)
    for repo in config.repos:
        assert isinstance(repo, str)
    assert isinstance(config.maintainers, list)
    for maintainer in config.maintainers:
        assert isinstance(maintainer, str)
    maintainers = config._load_maintainers()
    assert isinstance(maintainers, dict)
    for i in maintainers.items():
        assert isinstance(i[0], str)
        assert isinstance(i[1], list)
        for val in i[1]:
            assert isinstance(val, str)
    repos = config._load_repositories()
    assert isinstance(repos, dict)
    for i in repos.items():
        assert isinstance(i[0], str)
        assert isinstance(i[1], list)
        for val in i[1]:
            assert isinstance(val, str)


def test_cli(config):
    """Test cli commands."""
    pass
