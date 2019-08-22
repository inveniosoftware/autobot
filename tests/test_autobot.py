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

from mock import patch

from autobot.github import PR


def test_config(config):
    """Check configuration content."""
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


def test_bot_report(api):
    """Check the bot generated report."""
    pass


def test_issue_closed(issue_closed):
    """Check closed issue."""
    assert isinstance(issue_closed.maintainers, list)
    assert isinstance(issue_closed.actions, list)
    assert isinstance(issue_closed.info, dict)
    assert isinstance(issue_closed.status, dict)
    assert not issue_closed.status["is_open"]
    assert issue_closed.status["can_close"]
    assert not issue_closed.status["needs_comment"]
    assert "RFC" not in issue_closed.status["lbls"]
    assert not issue_closed.actions


def test_issue_close_1(issue_close_1):
    """Check issue that should be closed."""
    assert isinstance(issue_close_1.maintainers, list)
    assert isinstance(issue_close_1.actions, list)
    assert isinstance(issue_close_1.info, dict)
    assert isinstance(issue_close_1.status, dict)
    assert issue_close_1.status["is_open"]
    assert issue_close_1.status["can_close"]
    assert issue_close_1.status["needs_comment"]
    assert "RFC" not in issue_close_1.status["lbls"]
    assert len(issue_close_1.actions) == 1
    assert issue_close_1.actions[0] == "Close this!"


def test_issue_RFC_1(issue_RFC_1):
    """Check issue that should not be closed due to RFC label."""
    assert isinstance(issue_RFC_1.maintainers, list)
    assert isinstance(issue_RFC_1.actions, list)
    assert isinstance(issue_RFC_1.info, dict)
    assert isinstance(issue_RFC_1.status, dict)
    assert issue_RFC_1.status["is_open"]
    assert issue_RFC_1.status["can_close"]
    assert issue_RFC_1.status["needs_comment"]
    assert "RFC" in issue_RFC_1.status["lbls"]
    assert len(issue_RFC_1.actions) == 1
    assert issue_RFC_1.actions[0] == "Comment on this!"


def test_issue_review_1(issue_review_1):
    """Check issue that has pull request that needs review."""
    assert isinstance(issue_review_1.actions, list)
    assert isinstance(issue_review_1.maintainers, list)
    assert isinstance(issue_review_1.info, dict)
    assert isinstance(issue_review_1.status, dict)
    assert issue_review_1.status["is_open"]
    assert not issue_review_1.status["can_close"]
    assert not issue_review_1.status["needs_comment"]
    assert "RFC" not in issue_review_1.status["lbls"]
    assert not issue_review_1.actions


def test_issue_comment_1(issue_comment_1):
    """Check issue that needs comment."""
    assert isinstance(issue_comment_1.actions, list)
    assert isinstance(issue_comment_1.maintainers, list)
    assert isinstance(issue_comment_1.info, dict)
    assert isinstance(issue_comment_1.status, dict)
    assert issue_comment_1.status["is_open"]
    assert not issue_comment_1.status["can_close"]
    assert issue_comment_1.status["needs_comment"]
    assert "RFC" not in issue_comment_1.status["lbls"]
    assert len(issue_comment_1.actions) == 1
    assert issue_comment_1.actions[0] == "Comment on this!"


def test_pr_closed(pr_closed):
    """Check closed pull request."""
    assert isinstance(pr_closed.actions, list)
    assert isinstance(pr_closed.maintainers, list)
    assert isinstance(pr_closed.info, dict)
    assert isinstance(pr_closed.status, dict)
    assert not pr_closed.status["is_open"]
    assert pr_closed.status["can_close"]
    assert not pr_closed.status["needs_comment"]
    assert not pr_closed.status["needs_review"]
    with patch.object(PR, "can_merge", return_value=True):
        assert pr_closed.status["can_merge"]
        assert not pr_closed.actions
    # with patch.object(PR, 'can_merge', return_value=False):
    #     assert not pr_closed.status["can_merge"]
    #     assert not pr_closed.actions


def test_pr_close_1(pr_close_1):
    """Check pull request that should be closed."""
    assert isinstance(pr_close_1.actions, list)
    assert isinstance(pr_close_1.maintainers, list)
    assert isinstance(pr_close_1.info, dict)
    assert isinstance(pr_close_1.status, dict)
    assert pr_close_1.status["is_open"]
    assert pr_close_1.status["can_close"]
    assert pr_close_1.status["needs_comment"]
    assert not pr_close_1.status["needs_review"]
    with patch.object(PR, "can_merge", return_value=True):
        assert pr_close_1.status["can_merge"]
        assert len(pr_close_1.actions) == 1
        assert pr_close_1.actions[0] == "Merge this!"
    # with patch.object(PR, 'can_merge', return_value=False):
    #     assert not pr_close_1.status["can_merge"]
    #     assert len(pr_close_1.actions) == 1
    #     assert pr_close_1.actions[0] == "Close this!"


def test_pr_review_1(pr_review_1):
    """Check pull request that needs review."""
    assert isinstance(pr_review_1.actions, list)
    assert isinstance(pr_review_1.maintainers, list)
    assert isinstance(pr_review_1.info, dict)
    assert isinstance(pr_review_1.status, dict)
    assert pr_review_1.status["is_open"]
    assert not pr_review_1.status["can_close"]
    assert not pr_review_1.status["needs_comment"]
    assert pr_review_1.status["needs_review"]
    with patch.object(PR, "can_merge", return_value=True):
        assert pr_review_1.status["can_merge"]
        assert len(pr_review_1.actions) == 1
        assert pr_review_1.actions[0] == "Review this!"
    # with patch.object(PR, 'can_merge', return_value=False):
    #     assert not pr_review_1.status["can_merge"]
    #     assert len(pr_review_1.actions) == 1
    #     assert pr_review_1.actions[0] == "Review this!"


def test_pr_comment_1(pr_comment_1):
    """Check pull request that needs comment."""
    assert isinstance(pr_comment_1.actions, list)
    assert isinstance(pr_comment_1.maintainers, list)
    assert isinstance(pr_comment_1.info, dict)
    assert isinstance(pr_comment_1.status, dict)
    assert pr_comment_1.status["is_open"]
    assert not pr_comment_1.status["can_close"]
    assert pr_comment_1.status["needs_comment"]
    assert not pr_comment_1.status["needs_review"]
    with patch.object(PR, "can_merge", return_value=True):
        assert pr_comment_1.status["can_merge"]
        assert len(pr_comment_1.actions) == 2
        assert "Comment on this!" in pr_comment_1.actions
        assert "Merge this!" in pr_comment_1.actions
    # with patch.object(PR, 'can_merge', return_value=False):
    #     assert not pr_review_1.status["can_merge"]
    #     assert len(pr_review_1.actions) == 1
    #     assert pr_review_1.actions[0] == "Review this!"
