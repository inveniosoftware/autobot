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
from github3.pulls import ShortPullRequest
from lazy_load import lazy_func

from autobot.config_loader import Config


# class GitHubAPI:
#     """Perform requests for the target repositories."""

#     def __init__(self, owner, gh_token):
#         """Github client initialization."""
#         self.OWNER = owner
#         self.GH_CLIENT = login(token=gh_token)

#     @classmethod
#     def fetch_comment_info(cls, comment):
#         """Fetch information for a comment."""
#         return {
#             "url": comment.html_url,
#             "creation_date": comment.created_at,
#             "user": {"name": comment.user.login, "url": comment.user.html_url},
#         }

#     @classmethod
#     def fetch_pr_info(cls, pr):
#         """Fetch information for a pull request."""
#         return {
#             "id": pr.number,
#             "url": pr.html_url,
#             "title": pr.title,
#             "creation_date": pr.created_at,
#             "description": pr.body,
#             "state": pr.state,
#             "user": {"name": pr.user.login, "url": pr.user.html_url},
#             "related_issue": pr.issue_url,
#         }

#     @classmethod
#     def fetch_issue_info(cls, issue):
#         """Fetch information for an issue."""
#         return {
#             "id": issue.number,
#             "url": issue.html_url,
#             "title": issue.title,
#             "creation_date": issue.created_at,
#             "description": issue.body,
#             "state": issue.state,
#             "labels": [
#                 {"name": label.name, "color": label.color, "url": label.url}
#                 for label in issue.labels()
#             ],
#             "user": {"name": issue.user.login, "url": issue.user.html_url},
#         }

#     @classmethod
#     def fetch_repo_info(cls, repo):
#         """Fetch information for a repository."""
#         return {
#             "url": repo.html_url,
#             "creation_date": repo.created_at,
#             "description": repo.description,
#         }

#     @classmethod
#     def check_mentions(cls, m, maintainers):
#         """Check if someone in `maintainers` list was mentioned in `m`."""
#         res = []
#         mentions = list(
#             filter(
#                 lambda login: m.body
#                 and (
#                     login in [mention[1:] for mention in m.body if (mention[0] == "@")]
#                 ),
#                 maintainers,
#             )
#         )
#         if mentions:
#             res.append({"You've been mentioned here!": mentions})
#         return res

#     @classmethod
#     def check_mergeable(cls, pr, maintainers):
#         """Check if pull request `pr` is mergeable."""
#         res = []
#         if pr.refresh().mergeable:
#             res.append({"Merge this!": maintainers})
#         return res

#     @classmethod
#     def check_review(cls, pr, maintainers):
#         """Check if pull request `pr` needs a review."""
#         res = []
#         requested_reviewers = list(
#             filter(
#                 lambda login: login
#                 in [reviewer.login for reviewer in pr.requested_reviewers],
#                 maintainers,
#             )
#         )
#         if requested_reviewers:
#             res.append({"Review this!": requested_reviewers})
#         return res

#     @classmethod
#     def check_if_connected_to_issue(cls, pr, maintainers):
#         """Check if pull request `pr` is connected to some issue."""
#         res = []
#         if pr.issue() is None:
#             res.append({"Resolve not connected to issue!": maintainers})
#         return res

#     @classmethod
#     def check_close(cls, pr, maintainers):
#         """Check if pull request `pr` should be closed due to inaction."""
#         res = []
#         if (datetime.utcnow().replace(tzinfo=pytz.utc) - pr.updated_at).days >= 3 * 30:
#             res.append({"Close this!": maintainers})
#         return res

#     @classmethod
#     def check_follow_up(cls, pr, maintainers):
#         """Check if someone should follow up on pull request `pr` due to inaction."""
#         res = []
#         if ("WIP" in pr.title) and (
#             (datetime.utcnow().replace(tzinfo=pytz.utc) - pr.updated_at).days >= 1 * 30
#         ):
#             res.append({"Follow up on this!": maintainers})
#         return res

#     @classmethod
#     def check_labels(cls, issue, maintainers):
#         """Check issue's `issue` labels."""
#         res = []
#         if "RFC" in [label.name for label in issue.labels()]:
#             res.append({"Skip this for now!": maintainers})
#         return res

#     @classmethod
#     def check_comments(cls, issue, maintainers):
#         """Check if a response for an issue's `issue` comment is needed."""
#         res = []
#         comments = [comment for comment in issue.comments()]
#         if comments and comments[-1].user.login not in maintainers:
#             res.append({"Follow up on this!": maintainers})
#         return res

#     @classmethod
#     def comment_report(cls, comment, maintainers):
#         """Check a comment for possible actions."""
#         res = []
#         for f in comment_filters:
#             res += f(comment, maintainers)
#         return res

#     @classmethod
#     def pr_report(cls, pr, maintainers):
#         """Check a pull request for possible actions."""
#         res = []
#         for f in pr_filters:
#             res += f(pr, maintainers)
#         actions = {"review_comments": []}
#         for comment in pr.review_comments():
#             report = cls.comment_report(comment, maintainers)
#             actions["review_comments"].append(
#                 {**{"actions": report}, **cls.fetch_comment_info(comment)}
#             ) if report else None
#         res.append(actions) if actions["review_comments"] else None
#         actions = {"issue_comments": []}
#         for comment in pr.issue_comments():
#             report = cls.comment_report(comment, maintainers)
#             actions["issue_comments"].append(
#                 {**{"actions": report}, **cls.fetch_comment_info(comment)}
#             ) if report else None
#         res.append(actions) if actions["issue_comments"] else None
#         return res

#     @classmethod
#     def issue_report(cls, issue, maintainers):
#         """Check an issue for possible actions."""
#         res = []
#         for f in issue_filters:
#             res += f(issue, maintainers)
#         actions = {"comments": []}
#         for comment in issue.comments():
#             report = cls.comment_report(comment, maintainers)
#             actions["comments"].append(
#                 {**{"actions": report}, **cls.fetch_comment_info(comment)}
#             ) if report else None
#         res.append(actions) if actions["comments"] else None
#         return res

#     @classmethod
#     def repo_report(cls, repo, maintainers):
#         """Check a repository for possible actions."""
#         res = []
#         actions = {"prs": []}
#         for pr in repo.pull_requests():
#             if pr.state != "open":
#                 continue
#             report = cls.pr_report(pr, maintainers)
#             actions["prs"].append(
#                 {**{"actions": report}, **cls.fetch_pr_info(pr)}
#             ) if report else None
#         res.append(actions) if actions["prs"] else None
#         actions = {"issues": []}
#         for issue in repo.issues():
#             if issue.state != "open":
#                 continue
#             report = cls.issue_report(issue, maintainers)
#             actions["issues"].append(
#                 {**{"actions": report}, **cls.fetch_issue_info(issue)}
#             ) if report else None
#         res.append(actions) if actions["issues"] else None
#         return res

#     @lazy_func
#     def report(self, repos):
#         """Check repositories `repos` for possible actions."""
#         res = []
#         actions = {"repos": []}
#         for repo in repos:
#             repo_obj = self.GH_CLIENT.repository(self.OWNER, repo)
#             report = self.repo_report(repo_obj, repos[repo])
#             actions["repos"].append(
#                 {**{"actions": report}, **self.fetch_repo_info(repo_obj)}
#             ) if report else None
#         res.append(actions) if actions["repos"] else None
#         return res


# comment_filters = [GitHubAPI.check_mentions]

# pr_filters = [
#     GitHubAPI.check_mergeable,
#     GitHubAPI.check_review,
#     GitHubAPI.check_if_connected_to_issue,
#     GitHubAPI.check_mentions,
#     GitHubAPI.check_close,
#     GitHubAPI.check_follow_up,
# ]

# issue_filters = [
#     GitHubAPI.check_labels,
#     GitHubAPI.check_comments,
#     GitHubAPI.check_mentions,
# ]

class PR:
    """Pull request wrapper."""

    def __init__(self, pr):
        """Pull request wrapper object initialization."""
        self.pr = pr

    @property
    def info(self):
        """Fetch information for the pull request."""
        return {
            "id": self.pr.number,
            "url": self.pr.html_url,
            "title": self.pr.title,
            "creation_date": self.pr.created_at,
            "description": self.pr.body,
            "state": self.pr.state,
            "user": {"name": self.pr.user.login, "url": self.pr.user.html_url},
            "related_issue": self.pr.issue_url,
        }

    def can_merge(self):
        sha = self.pr.statuses_url.rsplit('/', 1)[-1]
        statuses = list(pr.repository.statuses(sha))
        return "error" in [s.state for s in statuses]

    filters = [
        can_merge,
        # needs_review,
        # can_close,
        # labels,
        # has_last_comment_from_maintainer,
    ]

    @property
    def status(self):
        status = {}
        for f in self.filters:
            status[f.__name__] = f(pr)
        return status

    @property
    def actions(self):
        pass

class Issue:
    """Issue wrapper object."""

    def __init__(self, issue, actions=[], status={}):
        """Pull Request initialization."""
        self.issue = issue
        self.actions = actions
        self.status = status

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
    def pr_info(cls, pr):
        """Fetch information for a pull request."""
        return {
            "id": pr.number,
            "url": pr.html_url,
            "title": pr.title,
            "creation_date": pr.created_at,
            "description": pr.body,
            "state": pr.state,
            "user": {"name": pr.user.login, "url": pr.user.html_url},
            "related_issue": pr.issue_url,
        }

    @classmethod
    def issue_info(cls, issue):
        """Fetch information for an issue."""
        return {
            "id": issue.number,
            "url": issue.html_url,
            "title": issue.title,
            "creation_date": issue.created_at,
            "description": issue.body,
            "state": issue.state,
            "labels": [
                {"name": label.name, "color": label.color, "url": label.url}
                for label in issue.labels()
            ],
            "user": {"name": issue.user.login, "url": issue.user.html_url},
        }

    @classmethod
    def repo_info(cls, repo):
        """Fetch information for a repository."""
        return {
            "url": repo.html_url,
            "creation_date": repo.created_at,
            "description": repo.description,
        }

    def can_merge(self, pr):
        sha = pr.statuses_url.rsplit('/', 1)[-1]
        statuses = list(pr.repository.statuses(sha))
        return "error" in [s.state for s in statuses]

    # def needs_review(self, pr):
    #     pass

    # def can_close(self, pr):
    #     pass

    @classmethod
    def repo_report(cls, repo, maintainers):
        """Check a repository for possible actions."""
        repo_report = {}
        for pr in repo.pull_requests():
            if pr.state != "open":
                continue
            status = {
                'can_merge': True,
                # 'needs_review': True,
                # 'can_close': True,
                # 'labels': [...],
                # 'has_last_comment_from_maintainer': False,
            }
            info = cls.pr_info(pr)
            pr_wrapper = PR(pr)
        for issue in repo.issues():
            if issue.state != "open":
                continue
            issue_status = {
                'can_merge': True,
                # 'needs_review': True,
                # 'can_close': True,
                # 'labels': [...],
                # 'has_last_comment_from_maintainer': False,
            }
            issue_actions = cls.issue_actions(issue, maintainers)
            issue_info = cls.issue_info(issue)
        return report

    @lazy_func
    def report(self):
        """Check repositories `repos` for possible actions."""
        report = {}
        for repo in self.repositories.keys():
            repo_obj = self.gh.repository(self.owner, repo)
            repo_report = self.repo_report(repo_obj, self.repositories[repo])
            if repo_report:
                report[repo] = self.repo_info(repo_obj)
                report[repo]["actions"] = repo_report
        return actions

    pr_filters = [
        can_merge,
        # needs_review,
        # can_close,
        # labels,
        # has_last_comment_from_maintainer,
    ]

    issue_filters = [
        can_merge,
        # needs_review,
        # can_close,
        # labels,
        # has_last_comment_from_maintainer,
    ]

# TODO:
# s = {
#     'can_merge': True,
#     'needs_review': True,
#     'can_close': True,
#     'labels': [...],
#     'has_last_comment_from_maintainer': False,
# }

# if s['can_merge'] and not s['need_review']:
#     return 'Merge this!'
# if s['can_close'] and not 'RFC' in s['labels']:
#     return 'Close this!'
