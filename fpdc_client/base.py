from collections.abc import MutableMapping

import coreapi

from .pagination import Paginator


DEFAULT_URL = "https://fpdc.fedoraproject.org/"

# Cache the server instance.
_server = None


def _check_server():
    global _server
    if _server is not None:
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
        global _server
        self.schema = self.client.get("http://localhost:8000/")
        _server = self


class APIObject(MutableMapping):

    api_endpoint = None
    api_id = None

    def __init__(self, data):
        if self.api_endpoint is None or self.api_id is None:
            raise NotImplementedError
        self.data = data

    def __repr__(self):
        return '<{name} "{id}">'.format(
            name=self.__class__.__name__, id=self.data.get(self.api_id)
        )

    def __str__(self):
        return str(dict(self.data))

    @classmethod
    def all(cls, page=1):
        _check_server()
        paginator = Paginator()
        while paginator.results_left:
            result = _server.client.action(
                _server.schema, [cls.api_endpoint, "list"], params={"page": page}
            )
            paginator.read_results(result)
            yield from [cls(data=data) for data in result["results"]]
            page = page + 1

    @classmethod
    def read(cls, **kwargs):
        _check_server()
        result = _server.client.action(
            _server.schema, [cls.api_endpoint, "read"], params=kwargs
        )
        return cls(data=result)

    @classmethod
    def create(cls, data):
        _check_server()
        result = _server.client.action(
            _server.schema, [cls.api_endpoint, "create"], params=data
        )
        return cls(data=result)

    def save(self):
        _check_server()
        result = _server.client.action(
            _server.schema, [self.api_endpoint, "update"], params=dict(self.data)
        )
        self.data = result

    def delete(self):
        _check_server()
        _server.client.action(
            _server.schema,
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
