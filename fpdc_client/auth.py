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

"""Authentication mechanism."""

from fedora.client.openidcclient import OpenIDCBaseClient
from requests.adapters import HTTPAdapter


class FedoraOIDCAdapter(HTTPAdapter):
    """Request adapter to add OIDC authentication.

    Args:
        app_id (str): The OpenID Connect application name. You may change it by
            subclassing or right after instanciation. It needs to be a valid
            linux filename, without slashes.
        config (dict): The client configuration as obtained during registration.
    """

    _scopes = [
        "openid",
        "profile",
        "email",
        "https://fpdc.fedoraproject.org/oidc/create-release",
        "https://id.fedoraproject.org/scope/groups",
    ]

    def __init__(self, app_id, config):
        super().__init__()
        id_provider = config["issuer"]
        client_id = config["client_id"]
        self._oidc_client = OpenIDCBaseClient(
            app_id, id_provider, client_id, client_secret=config["client_secret"]
        )

    def send(self, request, **kwargs):
        # TODO: dynamically add scopes depending on the request URL.
        token = self._oidc_client.get_token(self._scopes)
        request.headers.update({"Authorization": "Bearer {}".format(token)})
        return super().send(request, **kwargs)
