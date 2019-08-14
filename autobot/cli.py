#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2018 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI commands."""

import os
import sys

import click
from github3 import login, repository

from autobot.api import BotAPI
from autobot.config_loader import Config

dotenv_path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), ".env")

ini_path = os.path.join(os.path.abspath(os.path.join(__file__, "..")), "config.ini")


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def main():
    """Autobot CLI."""
    pass


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def report():
    """Autobot report CLI."""
    pass


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--owner",
    default="inveniosoftware",
    help="The repo owner/organization the service is offered to.",
)
@click.option(
    "--repo", multiple=True, help="The repositories to check for notifications."
)
@click.option("--maintainer", multiple=True, help="The maintainers to notify.")
@click.option("--format", default="json", help="The report format.")
def show(owner, repo, maintainer, format):
    """Autobot report show CLI."""
    conf = Config.load(
        AUTOBOT_OWNER=owner,
        AUTOBOT_REPOS=[r for r in repo],
        AUTOBOT_MAINTAINERS=[m for m in maintainer],
        env=dotenv_path,
        ini=ini_path,
        defaults=True,
    )
    bot = BotAPI(conf)
    res = bot.formatted_report(format)
    print(res)
    return 0


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--owner",
    default="inveniosoftware",
    help="The repo owner/organization the service is offered to.",
)
@click.option(
    "--repo", multiple=True, help="The repositories to check for notifications."
)
@click.option("--maintainer", multiple=True, help="The maintainers to notify.")
@click.option(
    "--via", default="gitter", help="Resource used for notification dispatch."
)
def send(owner, repo, maintainer, via):
    """Autobot report send CLI."""
    conf = Config.load(
        AUTOBOT_OWNER=owner,
        AUTOBOT_REPOS=[r for r in repo],
        AUTOBOT_MAINTAINERS=[m for m in maintainer],
        env=dotenv_path,
        ini=ini_path,
        defaults=True,
    )
    bot = BotAPI(conf)
    for m in conf.maintainers.keys():
        if via == "gitter":
            res = bot.send_report(m, "markdown")
            print(res)
    return 0


main.add_command(report)

report.add_command(show)
report.add_command(send)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
