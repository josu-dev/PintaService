class BaseService:
    """Base service class for all services.

    A service is a class that encapsulates business logic and
    exposes it through a public interface.
    """

    ...


class BaseServiceError(Exception):
    """Base service error class for all services.

    A service error is an exception that is raised when a service
    fails to execute its business logic.

    Attributes:
        message: A human-readable message describing the error.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
