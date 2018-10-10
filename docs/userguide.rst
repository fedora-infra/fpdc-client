User Guide
==========

Connecting
----------

Import the main ``FPDC`` class and instanciate it, passing a custom URL if
necessary:

>>> from fpdc_client import FPDC
>>> server = FPDC(url="http://localhost:8000/")

Now connect to the server. This will fetch the available actions from FPDC:

>>> server.connect()


Getting data
------------

Import the endpoint class(es) you want to work with:

>>> from fpdc_client import Release

You can retrieve all the releases from the server with:

>>> releases = Release.all()
>>> for r in releases:
...     print(r)

You can retrieve a single release with:

>>> release = Release.read({"release_id": "fedora-28"})

You can access the release's properties as a dict:

>>> release["release_id"]
"fedora-28"
>>> release["short"]
"fedora"
>>> release["version"]
"28"
>>> release["release_type"]
"ga"

All the data that has been retrieved from the server is available as a
``.data`` attribute:

>>> release.data
{...}


Making changes
--------------

If you have the right permissions, you can create a release with the following
call:

>>> new_release = Release.create(
...    {
...        "release_id": "fedora-42",
...        "short": "f42",
...        "version": "42",
...        "name": "Fedora",
...        "release_date": "2042-01-01",
...        "eol_date": "2042-12-31",
...        "sigkey": "towel",
...    }
... )

You can change the release properties as if it was a simple dictionary, but you
need to call the ``save()`` method to commit those changes to the server:

>>> new_release["name"] = "Don't Panic"
>>> new_release.save()

If you don't call ``save()``, the changes will be lost.
