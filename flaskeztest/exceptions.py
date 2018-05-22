
class PyEnvNotTestError(BaseException):
    DEFAULT_MESSAGE = "PY_ENV entry in flask app config dict not set to test."

    def __init__(self, message=DEFAULT_MESSAGE):
        BaseException.__init__(self, message)


class EztestidNotInFixture(BaseException):
    DEFAULT_MESSAGE = "Cannot test an element with an eztestid that was not loaded in a fixture yet."
    MESSAGE_FORMAT = "Cannot test an element with eztestid=\"%s\" that was not loaded in a fixture yet."

    def __init__(self, eztestid=None):
        if eztestid is None:
            message = self.DEFAULT_MESSAGE
        else:
            message = self.MESSAGE_FORMAT % eztestid
        BaseException.__init__(self, message)


class FixtureDoesNotExistError(BaseException):
    MESSAGE_FORMAT = "Cannot find a fixture json file in \"%s\" with name=\"%s\"."

    def __init__(self, fix_dir, fix_name):
        BaseException.__init__(self, self.MESSAGE_FORMAT % (fix_dir, fix_name))
