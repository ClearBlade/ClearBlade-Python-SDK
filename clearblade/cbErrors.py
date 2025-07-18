# To use cbErrors do the following:
# 1. In your code, import cbErrors
# 2. If the default error handling mechanism (i.e. simply exit) is all you need, then call cbErrors.handle(code) where needed.
# 3. If you need a different error handling mechanism then set cbErrors.ERROR_HANDLER to an object of your own error handler class.
# Your error handler class will inherit from ErrorHandler and can override the handle method.

from __future__ import print_function, absolute_import

class ErrorHandler:
    def handle(self, code):
        exit(code)

ERROR_HANDLER = ErrorHandler()

def handle(code):
    ERROR_HANDLER.handle(code)