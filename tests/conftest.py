# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2019 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test configuration file."""

import pytest
import yaml


@pytest.fixture(scope="session")
def info(tmpdir_factory):
    """Mock info for configuration testing."""
    mock = {
        "orgs": {
            "org1": {
                "repositories": {
                    "org1foo1": {
                        "description": "Description for org1foo1",
                        "maintainers": ["org1foo", "mix1"],
                    },
                    "org1foo2": {
                        "description": "Description for org1foo2",
                        "maintainers": ["org1foo", "mix2", "mix3"],
                    },
                    "org1foo3": {
                        "description": "Description for org1foo3",
                        "maintainers": ["org1foo", "mix1", "mix3"],
                    },
                    "org1bar1": {
                        "description": "Description for org1bar1",
                        "maintainers": ["org1bar", "mix1"],
                    },
                    "org1bar2": {
                        "description": "Description for org1bar2",
                        "maintainers": ["org1bar", "mix2"],
                    },
                    "org1baz1": {
                        "description": "Description for org1baz1",
                        "maintainers": ["org1baz", "mix2", "mix3"],
                    },
                }
            },
            "org2": {
                "repositories": {
                    "org2foo1": {
                        "description": "Description for org2foo1",
                        "maintainers": ["org2foo", "mix3"],
                    },
                    "org2bar1": {
                        "description": "Description for org2bar1",
                        "maintainers": ["org2bar", "mix1"],
                    },
                    "org2bar2": {
                        "description": "Description for org2bar2",
                        "maintainers": ["org2bar", "mix1", "mix2"],
                    },
                    "org2baz1": {
                        "description": "Description for org2baz1",
                        "maintainers": ["org2baz", "mix2", "mix3"],
                    },
                    "org2baz2": {
                        "description": "Description for org2baz2",
                        "maintainers": ["org2baz", "mix1"],
                    },
                }
            },
        }
    }
    d = tmpdir_factory.mktemp("tests").join("repositories.yml")
    with open(d, "w") as outfile:
        yaml.dump(mock, outfile, default_flow_style=False)
    return str(d)


@pytest.fixture
def config(info):
    """Configuration testing fixture."""
    from autobot.config_loader import Config

    return Config(
        AUTOBOT_OWNER="org1",
        AUTOBOT_INFO_PATH=info,
        AUTOBOT_GH_TOKEN="some gh token",
        AUTOBOT_GITTER_TOKEN="some gitter token",
    ).config
