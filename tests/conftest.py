# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2019 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test configuration file."""

from datetime import datetime

import pytest
import pytz
import yaml
from mock import MagicMock

from autobot.github import PR, Issue


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
        ini=True,
    )


@pytest.fixture
def api(config):
    """Bot API testing fixture."""
    from autobot.config_loader import Config
    from autobot.api import BotAPI

    return BotAPI(config)


@pytest.fixture
def user_1():
    """User 1 test case."""
    return MagicMock(**{"login": "user_1", "html_url": "user/1/url"})


@pytest.fixture
def user_2():
    """User 2 test case."""
    return MagicMock(**{"login": "user_2", "html_url": "user/2/url"})


@pytest.fixture
def user_3():
    """User 3 test case."""
    return MagicMock(**{"login": "user_3", "html_url": "user/3/url"})


@pytest.fixture
def user_4():
    """User 4 test case."""
    return MagicMock(**{"login": "user_4", "html_url": "user/4/url"})


@pytest.fixture
def comment_1(user_1):
    """Comment by user 1."""
    return MagicMock(**{"user": user_1})


@pytest.fixture
def comment_2(user_2):
    """Comment by user 2."""
    return MagicMock(**{"user": user_2})


@pytest.fixture
def comment_3(user_3):
    """Comment by user 3."""
    return MagicMock(**{"user": user_3})


@pytest.fixture
def comment_4(user_4):
    """Comment by user 4."""
    return MagicMock(**{"user": user_4})


@pytest.fixture
def label_1():
    """Label 1 test case."""
    label_1 = MagicMock()
    label_1.configure_mock(
        **{"name": "label_1", "color": "color_1", "url": "label/1/url"}
    )
    return label_1


@pytest.fixture
def label_2():
    """Label 2 test case."""
    label_2 = MagicMock()
    label_2.configure_mock(
        **{"name": "label_2", "color": "color_2", "url": "label/2/url"}
    )
    return label_2


@pytest.fixture
def label_3():
    """Label 3 test case."""
    label_3 = MagicMock()
    label_3.configure_mock(
        **{"name": "label_3", "color": "color_3", "url": "label/3/url"}
    )
    return label_3


@pytest.fixture
def label_RFC():
    """Label RFC test case."""
    label_RFC = MagicMock()
    label_RFC.configure_mock(
        **{"name": "RFC", "color": "color_RFC", "url": "label/RFC/url"}
    )
    return label_RFC


@pytest.fixture
def issue_closed(user_2, label_1, label_3):
    """Already closed issue."""
    return Issue(
        MagicMock(
            **{
                "number": 1,
                "html_url": "issue/closed/url",
                "title": "issue_closed",
                "created_at": datetime(year=2015, month=7, day=19, tzinfo=pytz.utc),
                "updated_at": datetime(year=2018, month=1, day=30, tzinfo=pytz.utc),
                "body": "Issue that is already closed.",
                "state": "closed",
                "user": user_2,
                "labels": lambda: [label_1, label_3],
                "comments": lambda: [],
            }
        ),
        ["user_1"],
    )


@pytest.fixture
def issue_close_1(user_1, label_1, label_2, label_3, comment_1):
    """Issue that needs to be closed."""
    return Issue(
        MagicMock(
            **{
                "number": 2,
                "html_url": "issue/close/1/url",
                "title": "issue_close_1",
                "created_at": datetime(year=2015, month=7, day=19, tzinfo=pytz.utc),
                "updated_at": datetime(year=2018, month=1, day=30, tzinfo=pytz.utc),
                "body": "Issue that should be closed.",
                "state": "open",
                "user": user_1,
                "labels": lambda: [label_1, label_2, label_3],
                "comments": lambda: [comment_1],
            }
        ),
        ["user_2"],
    )


@pytest.fixture
def issue_RFC_1(user_3, label_RFC, label_3, comment_1, comment_3):
    """Issue that can't be closed due to RFC label."""
    return Issue(
        MagicMock(
            **{
                "number": 3,
                "html_url": "issue/RFC/1/url",
                "title": "issue_RFC_1",
                "created_at": datetime(year=2015, month=7, day=19, tzinfo=pytz.utc),
                "updated_at": datetime(year=2018, month=1, day=30, tzinfo=pytz.utc),
                "body": "Issue that shouldn't be closed because of RFC in labels.",
                "state": "open",
                "user": user_3,
                "labels": lambda: [label_RFC, label_3],
                "comments": lambda: [comment_1, comment_3],
            }
        ),
        ["user_1"],
    )


@pytest.fixture
def issue_review_1(user_2, label_3, comment_1):
    """Issue with pull request that needs review."""
    return Issue(
        MagicMock(
            **{
                "number": 4,
                "html_url": "issue/review/1/url",
                "title": "issue_review_1",
                "created_at": datetime(year=2016, month=7, day=19, tzinfo=pytz.utc),
                "updated_at": datetime(year=2019, month=8, day=5, tzinfo=pytz.utc),
                "body": "Issue that has pull request that needs review.",
                "state": "open",
                "user": user_2,
                "labels": lambda: [label_3],
                "comments": lambda: [comment_1],
            }
        ),
        ["user_1"],
    )


@pytest.fixture
def issue_comment_1(user_2, label_3, comment_1, comment_2):
    """Issue that needs comment."""
    return Issue(
        MagicMock(
            **{
                "number": 5,
                "html_url": "issue/comment/1/url",
                "title": "issue_comment_1",
                "created_at": datetime(year=2016, month=7, day=19, tzinfo=pytz.utc),
                "updated_at": datetime(year=2019, month=8, day=5, tzinfo=pytz.utc),
                "body": "Issue that needs comment.",
                "state": "open",
                "user": user_2,
                "labels": lambda: [label_3],
                "comments": lambda: [comment_1, comment_2],
            }
        ),
        ["user_1"],
    )


@pytest.fixture
def pr_closed(user_2):
    """Already closed pull request."""
    return PR(
        MagicMock(
            **{
                "number": 1,
                "html_url": "pr/closed/url",
                "title": "pr_closed",
                "created_at": datetime(year=2015, month=7, day=23, tzinfo=pytz.utc),
                "updated_at": datetime(year=2018, month=1, day=30, tzinfo=pytz.utc),
                "body": "Pull request that is already closed.",
                "state": "closed",
                "user": user_2,
                "issue_url": "issue/closed/url",
                "reviews": lambda: ["review1", "review2"],
                "comments": lambda: [],
            }
        ),
        ["user_1"],
    )


@pytest.fixture
def pr_close_1(user_1, comment_1):
    """Pull request that should be closed."""
    return PR(
        MagicMock(
            **{
                "number": 2,
                "html_url": "pr/close/1/url",
                "title": "pr_close_1",
                "created_at": datetime(year=2015, month=7, day=23, tzinfo=pytz.utc),
                "updated_at": datetime(year=2018, month=1, day=30, tzinfo=pytz.utc),
                "body": "Pull request that is already closed.",
                "state": "open",
                "user": user_1,
                "issue_url": "issue/close/1/url",
                "reviews": lambda: ["review1"],
                "comments": lambda: [comment_1],
            }
        ),
        ["user_2"],
    )


@pytest.fixture
def pr_review_1(user_2, comment_1):
    """Pull request that needs review."""
    return PR(
        MagicMock(
            **{
                "number": 3,
                "html_url": "pr/review/1/url",
                "title": "pr_review_1",
                "created_at": datetime(year=2016, month=7, day=23, tzinfo=pytz.utc),
                "updated_at": datetime(year=2019, month=8, day=5, tzinfo=pytz.utc),
                "body": "Pull request that needs review.",
                "state": "open",
                "user": user_2,
                "issue_url": "issue/review/1/url",
                "reviews": lambda: [],
                "comments": lambda: [comment_1],
            }
        ),
        ["user_1"],
    )


@pytest.fixture
def pr_comment_1(user_2, comment_1, comment_2):
    """Pull request that needs comment."""
    return PR(
        MagicMock(
            **{
                "number": 3,
                "html_url": "pr/review/1/url",
                "title": "pr_review_1",
                "created_at": datetime(year=2016, month=7, day=23, tzinfo=pytz.utc),
                "updated_at": datetime(year=2019, month=8, day=5, tzinfo=pytz.utc),
                "body": "Pull request that needs review.",
                "state": "open",
                "user": user_2,
                "issue_url": "issue/review/1/url",
                "reviews": lambda: ["review1"],
                "comments": lambda: [comment_1, comment_2],
            }
        ),
        ["user_1"],
    )
