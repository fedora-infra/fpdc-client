User Guide
==========

Connecting
----------

Import the main ``FPDC`` class and instanciate it, passing a custom URL if
necessary:

>>> from fpdc_client import FPDC
>>> server = FPDC(url="http://localhost:8000/")

.. note::

    By default the FPDC client will connect to the production server.
    You can use the STG_URL global variable to connect to the staging server.

Now connect to the server. This will fetch the available actions from FPDC:

>>> server.connect()


Authentication
--------------

The Fedora servers use OIDC to authenticate, you need to get a ``client_id``
and a corresponding secret from the OIDC server.

.. note::

    If you are using the production or staging instance of FPDC the client_id and
    client_secret are automatically provided.

During development, you can use dynamic registration on the development OIDC
server with the following command::

   pip install oidc-register
   oidc-register https://iddev.fedorainfracloud.org/openidc/ http://localhost:12345/ http://localhost:23456/

This will produce a ``client_secrets.json`` file. Then you can call the
:py:meth:`login` method passing it the path to this file::

>>> server.login(auth_file="client_secrets.json")

The first time, it will open a browser window on the OIDC provider, asking you
to login and to consent to the transmission of your personal information.

After this step, you can close the browser window, your client is
authenticated.


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
