#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2018 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from autobot.config import Config
from autobot.api import BotAPI
import sys
import yaml
import click
from github3 import login, repository


@click.group()
def main():
    pass


@click.group()
def report():
    pass


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--owner', default='inveniosoftware', help='The repo owner we plan to offer the service to.')
@click.option('--repo', multiple=True, help='The repositories to check for notifications.')
@click.option('--maintainer', multiple=True, help='The maintainers to notify.')
@click.option('--format', default='json', help='The result format.')
def show(owner, repo, maintainer, format):
    conf = Config(owner, repos=[r for r in repo], maintainers=[m for m in maintainer])
    bot = BotAPI(conf)
    for m in conf._load_maintainers().keys():
        res = bot.generate_report(m)
        with open('results.yml', 'w') as outfile:
            yaml.dump(res, outfile, default_flow_style=False)
        if format == 'json':
            print(res)
        elif format == 'yaml':
            print(yaml.dump(res))
    return 0


# @click.command(context_settings=dict(help_option_names=['-h', '--help']))
# @click.option('--owner', default='inveniosoftware', help='The repo owner we plan to offer the service to.')
# @click.option('--repo', multiple=True, help='The repositories to check for notifications.')
# @click.option('--maintainer', multiple=True, help='The maintainers to notify.')
# @click.option('--format', default='json', help='The result format.')
# def send(owner, repo, maintainer, format):
#     conf = Config(owner, repos=[r for r in repo], maintainers=[m for m in maintainer])
#     bot = BotAPI(conf)
#     res = bot.generate_report()
#     # with open('results.yml', 'w') as outfile:
#     #     yaml.dump(res, outfile, default_flow_style=False)
#     if format == 'json':
#         print(res)
#     elif format == 'yaml':
#         print(yaml.dump(res))
#     return 0


main.add_command(report)

report.add_command(show)
# report.add_command(send)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
