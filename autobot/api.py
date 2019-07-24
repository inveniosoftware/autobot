# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Autobot API."""

from autobot.config import Config
from autobot.github import GitHubAPI


class BotAPI:
    """Generates report."""

    def __init__(self, config: Config):
        self.config = config
        self.report = GitHubAPI(self.config)._report(self.config._load_repositories())

    def generate_report(self, maintainer: str) -> dict:
        """Generates a report for a maintainer."""

        res = self.report[0]["repos"]
        print(res)
        print(
            "---------------------------------------------------------------------------------"
        )
        return res

    def send_report(self, maintainer: str, format: str):
        """Send the report to a maintainer (on Gitter or via email)."""

        res = self.generate_report(maintainer)
        if format == "markdown":
            """ TO DO """
