"""All excpetions defined for the flaskeztest package defined here."""


class NotInitializedError(BaseException):
    """Raised when a method is called on a EZTester instance that has not been initialized with init_app() yet."""
    def __init__(self, message="EZTester instance not initialized with Flask app or SQLAlchemy DB yet."):
        BaseException.__init__(self, message)
