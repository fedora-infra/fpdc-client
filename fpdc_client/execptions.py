"""Exceptions raised by fpdc-client."""


class FPDCError(Exception):
    """The base class for all exceptions raised by fpdc-client."""


class PermissionDenied(FPDCError):
    """
    Raised when the client does not have the permission to execute an action
    on the server
    Args:
        message (str): A Description of which action was denied
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Permission  Denied: {self.message}"
