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
    "-o",
    default="inveniosoftware",
    help="The repo owner/organization the service is offered to.",
)
@click.option(
    "--repo", "-r", multiple=True, help="The repositories to check for notifications."
)
@click.option("--maintainer", "-m", multiple=True, help="The maintainers to notify.")
@click.option(
    "--dotenv_config",
    "-e",
    default=Config.dotenv_path,
    type=click.Path(),
    help="The .env file to load configurations.",
)
@click.option(
    "--ini_config",
    "-i",
    default=Config.ini_path,
    type=click.Path(),
    help="The .ini file to load configurations.",
)
@click.option("--format", "-f", default="json", help="The report format.")
def show(owner, repo, maintainer, dotenv_config, ini_config, format):
    """Autobot report show CLI."""
    conf = Config(
        AUTOBOT_OWNER=owner,
        AUTOBOT_REPOS=[r for r in repo],
        AUTOBOT_MAINTAINERS=[m for m in maintainer],
        dotenv=dotenv_config,
        ini=ini_config,
    )
    bot = BotAPI(conf)
    res = bot.format_report(format)
    print(res)
    return 0


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--owner",
    "-o",
    default="inveniosoftware",
    help="The repo owner/organization the service is offered to.",
)
@click.option(
    "--repo", "-r", multiple=True, help="The repositories to check for notifications."
)
@click.option("--maintainer", "-m", multiple=True, help="The maintainers to notify.")
@click.option(
    "--dotenv_config",
    "-e",
    default=True,
    type=click.Path(),
    help="The .env file to load configurations.",
)
@click.option(
    "--ini_config",
    "-i",
    default=True,
    type=click.Path(),
    help="The .ini file to load configurations.",
)
@click.option(
    "--via", "-v", default="gitter", help="Resource used for notification dispatch."
)
def send(owner, repo, maintainer, dotenv_config, ini_config, via):
    """Autobot report send CLI."""
    conf = Config(
        AUTOBOT_OWNER=owner,
        AUTOBOT_REPOS=[r for r in repo],
        AUTOBOT_MAINTAINERS=[m for m in maintainer],
        dotenv=dotenv_config,
        ini=ini_config,
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
