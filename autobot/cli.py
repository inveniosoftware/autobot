#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2018 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI commands."""

import sys

import click
import yaml
from github3 import login, repository

from autobot.api import BotAPI
from autobot.config import Config


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def main():
    """Autobot cli."""
    pass


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def report():
    """Autobot report cli."""
    pass


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--owner",
    default="inveniosoftware",
    help="The repo owner we plan to offer the service to.",
)
@click.option(
    "--repo", multiple=True, help="The repositories to check for notifications."
)
@click.option("--maintainer", multiple=True, help="The maintainers to notify.")
@click.option("--format", default="json", help="The result format.")
def show(owner, repo, maintainer, format):
    """Autobot report show cli."""
    conf = Config(
        owner=owner, repos=[r for r in repo], maintainers=[m for m in maintainer]
    )
    bot = BotAPI(conf)
    res = bot.report
    with open("results.yml", "w") as outfile:
        yaml.dump(res, outfile, default_flow_style=False)
    if format == "json":
        print(res)
    elif format == "yaml":
        print(yaml.dump(res))
    return 0


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--owner",
    default="inveniosoftware",
    help="The repo owner we plan to offer the service to.",
)
@click.option(
    "--repo", multiple=True, help="The repositories to check for notifications."
)
@click.option("--maintainer", multiple=True, help="The maintainers to notify.")
@click.option(
    "--via", default="gitter", help="Resource used for notification dispatch."
)
def send(owner, repo, maintainer, via):
    """Autobot report send cli."""
    conf = Config(
        owner=owner, repos=[r for r in repo], maintainers=[m for m in maintainer]
    )
    bot = BotAPI(conf)
    for m in conf._load_maintainers().keys():
        if via == "gitter":
            bot.send_report(m, "markdown")
    return 0


main.add_command(report)

report.add_command(show)
report.add_command(send)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
