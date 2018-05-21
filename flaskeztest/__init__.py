"""The flaskeztest package"""

import re
import functools


class EZTestTemplater(object):
    """Main flaskeztest class that will be used on the application side."""

    def __init__(self):
        self.app = None
        self.testing = None

    def init_app(self, app):
        self.app = app
        self.testing = app.config['PY_ENV'] == 'test'

        def eztestid_func(eztestid):
            # TODO: Add in index for table rows
            if self.testing:
                return '_eztestid=' + eztestid
            else:
                return ''

        def ctx_proc():
            return dict(_eztestid=eztestid_func)

        self.app.context_processor(ctx_proc)

