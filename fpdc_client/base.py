"""
This module contains the base classes that will be built upon to access API endpoints.
"""

from collections.abc import MutableMapping

import coreapi

from .pagination import Paginator


DEFAULT_URL = "https://fpdc.fedoraproject.org/"

# Cache the server instance for convenience.
_SERVER = None


def _check_server(server):
    if server is not None:
        return
    raise RuntimeError(
        "You must first create an instance of FPDC and call the connect() method."
    )


class FPDC:
    """Main class handling the connection to an FPDC server.

    Args:
        url (str, optional): The URL of the FPDC server.
    """

    def __init__(self, url=DEFAULT_URL):
        self.url = url
        self.client = coreapi.Client()
        self.schema = None

    def connect(self):
        """Connect to the FPDC server and retrieve the REST schema.

        This method must be called before any other operation is possible.
        """
        global _SERVER
        self.schema = self.client.get("http://localhost:8000/")
        _SERVER = self


class APIObject(MutableMapping):
    """Base class for REST endpoints.

    This class behaves like a dictionary: the endpoint's attributes are available as items.
    One exception though, if you modify an attribute, you have to call the :py:meth:`save`
    method to commit those changes to the server.

    Attributes:
        api_endpoint (str): the name of the REST API endpoint (e.g.: "release").
            It must be implemented by sub-classes.
        api_id (str): the endpoint's property to use as the unique identifier (e.g.: "release_id").
            It must be implemented by sub-classes.

    Args:
        data (dict): data provided by the REST server.
        server (:py:class:`FPDC`, optional): FPDC server, defaults to the last FPDC server that was
            connected to.

    Raises:
        NotImplementedError: raised if :py:attr:`api_endpoint` or :py:attr:`api_id` have not been
            implemented and are still ``None``.
    """

    api_endpoint = None
    api_id = None

    def __init__(self, data, server=None):
        if self.api_endpoint is None or self.api_id is None:
            raise NotImplementedError
        self._server = server or _SERVER
        self.data = data

    def __repr__(self):
        return '<{name} "{id}">'.format(
            name=self.__class__.__name__, id=self.data.get(self.api_id)
        )

    def __str__(self):
        return str(dict(self.data))

    @classmethod
    def all(cls, server=None):
        """Retrieve all instances of this endpoint from the server.

        Args:
            server (:py:class:`FPDC`, optional): FPDC server, defaults to the last FPDC server
                that was connected to.

        Yields:
            :py:class:`APIObject`: the next instance of this endpoint available on the server.
        """

        server = server or _SERVER
        _check_server(server)
        page = 1
        paginator = Paginator()
        while paginator.results_left:
            result = server.client.action(
                server.schema, [cls.api_endpoint, "list"], params={"page": page}
            )
            paginator.read_results(result)
            yield from [cls(data=data, server=server) for data in result["results"]]
            page = page + 1

    @classmethod
    def read(cls, params, server=None):
        """Retrieve a single instance of this endpoint from the server.

        Args:
            params (dict): Query elements to select the desired instance.
            server (:py:class:`FPDC`, optional): FPDC server, defaults to the last FPDC server
                that was connected to.

        Returns:
            :py:class:`APIObject`: The corresponding instance from the server.
        """

        server = server or _SERVER
        _check_server(server)
        result = server.client.action(
            server.schema, [cls.api_endpoint, "read"], params=params
        )
        return cls(data=result, server=server)

    @classmethod
    def create(cls, data, server=None):
        """Create an instance of this endpoint on the server.

        Args:
            data (dict): The instance's attributes.
            server (:py:class:`FPDC`, optional): FPDC server, defaults to the last FPDC server
                that was connected to.

        Returns:
            :py:class:`APIObject`: The newly created instance.
        """

        server = server or _SERVER
        _check_server(server)
        result = server.client.action(
            server.schema, [cls.api_endpoint, "create"], params=data
        )
        return cls(data=result, server=server)

    def save(self):
        """Save the modifications on the server.

        APIObject instances can be modified like a dictionary, but the changes are only committed
        to the server when the :py:meth:`save` method is called.
        """

        _check_server(self._server)
        result = self._server.client.action(
            self._server.schema, [self.api_endpoint, "update"], params=dict(self.data)
        )
        self.data = result

    def delete(self):
        """Delete the instance on the server.
        """

        _check_server(self._server)
        self._server.client.action(
            self._server.schema,
            [self.api_endpoint, "delete"],
            params={"id": self.data["id"]},  # Should we use self.api_id?
        )
        # Make sure the instance is unusable now.
        self.data = None

    # Behave like a dict

    def __getitem__(self, key):
        return self.data.__getitem__(key)

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)
        # We could do a partial_update here but I think explicitely calling save() is better.

    def __delitem__(self, key):
        return self.data.__delitem__(key)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return len(self.data)
