
class FixtureDoesNotExistError(BaseException):
    MESSAGE_FORMAT = "Cannot find a fixture json file in \"%s\" with name=\"%s\"."

    def __init__(self, fix_dir, fix_name):
        BaseException.__init__(self, self.MESSAGE_FORMAT % (fix_dir, fix_name))
