# -*- coding: utf-8 -*-
#
# This file is part of Autobot.
# Copyright (C) 2015-2019 CERN.
#
# Autobot is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""The details of the configuration options for Autobot (deafult values given)."""

AUTOBOT_GH_TOKEN = "CHANGE ME"
"""The github token used for making requests to the github API.

    It **must** be a none empty string corresponding to a valid github token.
"""

AUTOBOT_GITTER_TOKEN = "CHANGE ME"
"""The gitter token used for sending the generated report via gitter API.

    It **must** be a none empty string corresponding to a valid gitter token.
"""

AUTOBOT_INFO_PATH = "autobot/opensource/repositories.yml"
"""The path to the **yaml** file that contains the information about the organization we provide the service for.

    It **must** be a none empty string corresponding to the direcotry of a yaml file of the following structure:

    .. code-block:: python

    info = {
        "orgs": {
            "valid organization name here": {
                "repositories": {
                    "valid repository name here": {
                        "maintainers": # maintainers list,
                        "some attribute": # corresponding value,
                        "some other attribute": # corresponding value,
                        # and so on ...
                    },
                    "valid repository name here": {
                        "maintainers": # maintainers list,
                        "some attribute": # corresponding value,
                        "some other attribute": # corresponding value,
                        # and so on ...
                    },
                    # and so on ...
                }
            },
            "valid organization name here": {
                "repositories": {
                    "valid repository name here": {
                        "maintainers": # maintainer list,
                        "some attribute": # corresponding value,
                        "some other attribute": # corresponding value,
                        # and so on ...
                    },
                    "valid repository name here": {
                        "maintainers": # maintainer list,
                        "some attribute": # corresponding value,
                        "some other attribute": # corresponding value,
                        # and so on ...
                    },
                    # and so on ...
                }
            },
            # and so on ...
        }
    }
"""

# AUTOBOT_MAIL_SETTINGS={}

AUTOBOT_MAINTAINERS = []
"""A string list of the github users that are listed as maintainers (see ``AUTOBOT_INFO_PATH``) of the repositories of interest (see ``AUTOBOT_REPOS``).

    Every item of the list **must** be a none empty string corresponding to a valid github user.
"""

AUTOBOT_OWNER = "inveniosoftware"
"""The name of the organization we provide the service for.

    It **must** be a none empty string corresponding to a valid github user.
"""

AUTOBOT_REPOS = []
"""A string list of the github repositories to generate reports for.

    Every item of the list **must** be a none empty string corresponding to a valid github repository owned by ``AUTOBOT_OWNER``.
"""
