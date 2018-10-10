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
    def __init__(self, url=DEFAULT_URL):
        self.url = url
        self.client = coreapi.Client()
        self.schema = None

    def connect(self):
        global _SERVER
        self.schema = self.client.get("http://localhost:8000/")
        _SERVER = self


class APIObject(MutableMapping):

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
        server = server or _SERVER
        _check_server(server)
        result = server.client.action(
            server.schema, [cls.api_endpoint, "read"], params=params
        )
        return cls(data=result, server=server)

    @classmethod
    def create(cls, data, server=None):
        server = server or _SERVER
        _check_server(server)
        result = server.client.action(
            server.schema, [cls.api_endpoint, "create"], params=data
        )
        return cls(data=result, server=server)

    def save(self):
        _check_server(self._server)
        result = self._server.client.action(
            self._server.schema, [self.api_endpoint, "update"], params=dict(self.data)
        )
        self.data = result

    def delete(self):
        _check_server(self._server)
        self._server.client.action(
            self._server.schema,
            [self.api_endpoint, "delete"],
            params={"id": self.data["id"]},
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
