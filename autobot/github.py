# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Github Client."""

from datetime import datetime

import pytz
from github3 import login, repository
from lazy_load import lazy_func

from autobot.config_loader import Config


class GHWrapper:
    """GitHub object wrapper."""

    def __getattr__(self, attr):
        """Override __getattr__ method."""
        return getattr(self.__dict__, attr, getattr(self.__dict__["_gh_obj"], attr))


class PR(GHWrapper):
    """Pull request wrapper."""

    def __init__(self, pr, maintainers=None):
        """Pull request wrapper object initialization."""
        self._gh_obj = pr
        self.maintainers = maintainers

    @property
    def info(self):
        """Fetch information for the pull request."""
        return {
            "id": self.number,
            "url": self.html_url,
            "title": self.title,
            "creation_date": self.created_at,
            "description": self.body,
            "state": self.state,
            "user": {"name": self.user.login, "url": self.user.html_url},
            "related_issue": self.issue_url,
        }

    def is_open(self):
        """Check if puul request is open."""
        return self.state == "open"

    def can_close(self):
        """Check if pull request can be closed."""
        return (
            datetime.utcnow().replace(tzinfo=pytz.utc) - self.updated_at
        ).days >= 3 * 30

    def needs_comment(self):
        """Check if pull request needs comment."""
        comments = [comment for comment in self.review_comments()]
        return comments and comments[-1].user.login not in self.maintainers

    def can_merge(self):
        """Check if pull request can be merged."""
        sha = self.statuses_url.rsplit("/", 1)[-1]
        statuses = list(self.repository.statuses(sha))
        return "error" not in [s.state for s in statuses]

    def needs_review(self):
        """Check if pull request needs review."""
        reviews = [r for r in self.reviews()]
        return len(reviews) == 0

    filters = [is_open, can_close, needs_comment, can_merge, needs_review]

    @property
    def status(self):
        """The status of the pull request."""
        status = {}
        for f in self.filters:
            status[f.__name__] = f(self)
        return status

    @property
    def actions(self):
        """The suitable actions for the pull request."""
        actions = []
        # print(self.info)
        # print(self.is_open())
        # print(self.can_close())
        # print(self.needs_comment())
        # print(self.can_merge())
        # print(self.needs_review())
        # print(self.status["is_open"])
        if not self.status["is_open"]:
            return actions
        if not self.status["can_close"]:
            if self.status["needs_comment"]:
                actions.append("Comment on this!")
            if self.status["needs_review"]:
                actions.append("Review this!")
            elif self.status["can_merge"]:
                actions.append("Merge this!")
        else:
            if self.status["can_merge"] and not self.status["needs_review"]:
                actions.append("Merge this!")
            else:
                actions.append("Close this!")
        return actions


class Issue(GHWrapper):
    """Issue wrapper object."""

    def __init__(self, issue, maintainers=None):
        """Issue wrapper object initialization."""
        self._gh_obj = issue
        self.maintainers = maintainers

    @property
    def info(self):
        """Fetch information for an issue."""
        return {
            "id": self.number,
            "url": self.html_url,
            "title": self.title,
            "creation_date": self.created_at,
            "description": self.body,
            "state": self.state,
            "user": {"name": self.user.login, "url": self.user.html_url},
            "labels": [
                {"name": label.name, "color": label.color, "url": label.url}
                for label in self.labels()
            ],
        }

    def is_open(self):
        """Check if issue is open."""
        return self.state == "open"

    def can_close(self):
        """Check if issue can be closed."""
        return (
            datetime.utcnow().replace(tzinfo=pytz.utc) - self.updated_at
        ).days >= 3 * 30

    def needs_comment(self):
        """Check if issue needs comment."""
        comments = [comment for comment in self.comments()]
        return comments and comments[-1].user.login not in self.maintainers

    def lbls(self):
        """Fetch issue's labels."""
        return [l.name for l in self.labels()]

    filters = [is_open, can_close, needs_comment, lbls]

    @property
    def status(self):
        """The status of the issue."""
        status = {}
        for f in self.filters:
            status[f.__name__] = f(self)
        return status

    @property
    def actions(self):
        """The suitable actions for the issue."""
        actions = []
        if not self.status["is_open"]:
            return actions
        if self.status["can_close"] and not "RFC" in self.status["lbls"]:
            actions.append("Close this!")
        elif self.status["needs_comment"]:
            actions.append("Comment on this!")
        return actions


class GitHubAPI:
    """Perform requests for the target repositories."""

    def __init__(self, owner, gh_token, repositories):
        """Github client initialization."""
        self.owner = owner
        self.gh = login(token=gh_token)
        self.repositories = repositories

    @classmethod
    def comment_info(cls, comment):
        """Fetch information for a comment."""
        return {
            "url": comment.html_url,
            "creation_date": comment.created_at,
            "user": {"name": comment.user.login, "url": comment.user.html_url},
        }

    @classmethod
    def repo_info(cls, repo):
        """Fetch information for a repository."""
        return {
            "url": repo.html_url,
            "creation_date": repo.created_at,
            "description": repo.description,
        }

    @classmethod
    def repo_report(cls, repo, maintainers):
        """Check a repository for possible actions."""
        repo_report = {}
        for pr in repo.pull_requests():
            if pr.state != "open":
                continue
            pr_wrapper = PR(pr, maintainers)
            actions = pr_wrapper.actions
            for a in actions:
                if a not in repo_report.keys():
                    repo_report[a] = []
                repo_report[a].append(pr_wrapper.info)
        for issue in repo.issues():
            if issue.state != "open":
                continue
            issue_wrapper = Issue(issue, maintainers)
            actions = issue_wrapper.actions
            for a in actions:
                if a not in repo_report.keys():
                    repo_report[a] = []
                repo_report[a].append(issue_wrapper.info)
        return repo_report

    @lazy_func
    def report(self):
        """Check repositories for possible actions."""
        report = {}
        for repo in self.repositories.keys():
            repo_obj = self.gh.repository(self.owner, repo)
            maintainers = self.repositories[repo]
            repo_report = self.repo_report(repo_obj, maintainers)
            if repo_report:
                report[repo] = self.repo_info(repo_obj)
                report[repo]["maintainers"] = maintainers
                report[repo]["actions"] = repo_report
        return report
