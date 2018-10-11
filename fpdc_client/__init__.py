# This file is part of fpdc_client.
# Copyright (C) 2018 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""This module is where client code can import objects.

Attributes:
    FPDC: the :py:class:`FPDC` server class to instanciate first.
    Release: the :py:class:`release <Release>` REST endpoint.
"""

from .base import FPDC  # noqa:F401
from .endpoints import Release  # noqa:F401

__version__ = "0.1"
