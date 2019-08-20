# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Mocks for testing."""

from datetime import datetime

from mock import MagicMock

user_1 = MagicMock(spec_set={"login": "user_1", "html_url": "user/1/url"})

user_2 = MagicMock(spec_set={"login": "user_2", "html_url": "user/2/url"})

user_3 = MagicMock(spec_set={"login": "user_3", "html_url": "user/3/url"})

user_4 = MagicMock(spec_set={"login": "user_4", "html_url": "user/4/url"})

label_1 = MagicMock(
    spec_set={"name": "label_1", "color": "color_1", "url": "label/1/url"}
)

label_2 = MagicMock(
    spec_set={"name": "label_2", "color": "color_2", "url": "label/2/url"}
)

label_3 = MagicMock(
    spec_set={"name": "label_3", "color": "color_3", "url": "label/3/url"}
)

label_RFC = MagicMock(
    spec_set={"name": "RFC", "color": "color_RFC", "url": "label/RFC/url"}
)

issue_closed = MagicMock(
    spec_set={
        "number": 1,
        "html_url": "issue/closed/url",
        "title": "issue_closed",
        "created_at": datetime(year=2015, month=7, day=19),
        "updated_at": datetime(year=2018, month=1, day=30),
        "body": "Issue that is already closed.",
        "state": "closed",
        "user": user_2,
        "labels": [label_1, label_3],
    }
)

issue_close_1 = MagicMock(
    spec_set={
        "number": 2,
        "html_url": "issue/close/1/url",
        "title": "issue_close_1",
        "created_at": datetime(year=2015, month=7, day=19),
        "updated_at": datetime(year=2018, month=1, day=30),
        "body": "Issue that should be closed.",
        "state": "open",
        "user": user_1,
        "labels": [label_1, label_2, label_3],
    }
)

issue_RFC_1 = MagicMock(
    spec_set={
        "number": 3,
        "html_url": "issue/RFC/1/url",
        "title": "issue_RFC_1",
        "created_at": datetime(year=2015, month=7, day=19),
        "updated_at": datetime(year=2018, month=1, day=30),
        "body": "Issue that shouldn't be closed because of RFC in labels.",
        "state": "open",
        "user": user_3,
        "labels": [label_RFC, label_3],
    }
)

issue_review_1 = MagicMock(
    spec_set={
        "number": 4,
        "html_url": "issue/review/1/url",
        "title": "issue_review_1",
        "created_at": datetime(year=2016, month=7, day=19),
        "updated_at": datetime(year=2019, month=8, day=5),
        "body": "Issue that has pull request that needs review.",
        "state": "open",
        "user": user_2,
        "labels": [label_3],
    }
)

pr_closed = MagicMock(
    spec_set={
        "number": 1,
        "html_url": "pr/closed/url",
        "title": "pr_closed",
        "created_at": datetime(year=2015, month=7, day=23),
        "updated_at": datetime(year=2018, month=1, day=30),
        "body": "Pull request that is already closed.",
        "state": "closed",
        "user": user_2,
        "issue_url": "issue/closed/url",
        "reviews": ["review1", "review2"],
    }
)

pr_close_1 = MagicMock(
    spec_set={
        "number": 2,
        "html_url": "pr/close/1/url",
        "title": "pr_close_1",
        "created_at": datetime(year=2015, month=7, day=23),
        "updated_at": datetime(year=2018, month=1, day=30),
        "body": "Pull request that is already closed.",
        "state": "open",
        "user": user_1,
        "issue_url": "issue/close/1/url",
        "reviews": ["review1"],
    }
)

pr_review_1 = MagicMock(
    spec_set={
        "number": 3,
        "html_url": "pr/review/1/url",
        "title": "pr_review_1",
        "created_at": datetime(year=2016, month=7, day=23),
        "updated_at": datetime(year=2019, month=8, day=5),
        "body": "Pull request that needs review.",
        "state": "open",
        "user": user_2,
        "issue_url": "issue/review/1/url",
        "reviews": [],
    }
)
