"""This module contains the REST API endpoint-specific classes.
"""

from .base import APIObject


class Release(APIObject):
    """API endpoint for releases."""

    api_endpoint = "release"
    api_id = "release_id"
