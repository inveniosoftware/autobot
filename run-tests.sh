#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2015-2019 CERN.
# SPDX-License-Identifier: MIT

black --check . && \
isort -c . && \
pydocstyle autobot tests docs && \
sphinx-build -qnNW docs docs/_build/html && \
pytest
