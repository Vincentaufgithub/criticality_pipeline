class MDRSException(Exception):
    """Thrown when some kind of errors occurred"""

    pass


class IllegalArgumentException(MDRSException):
    """Thrown when something wrong with the argument is passed to a method"""

    pass


class MissingConfigurationException(MDRSException):
    """Thrown when wrong or missing system configuration"""

    pass


class BadRequestException(MDRSException):
    """Thrown when the request does not contain valid parameter"""

    pass


class UnauthorizedException(MDRSException):
    """Thrown when the current user not allowed to perform an operation on the resource"""

    pass


class ForbiddenException(MDRSException):
    """Thrown when the current user does not have enough privileges to access the resource"""

    pass


class UnexpectedException(MDRSException):
    """Thrown when unexpected error occurred"""

    pass
