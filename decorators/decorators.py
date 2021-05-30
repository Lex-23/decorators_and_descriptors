import types
from typing import Any, Dict
from functools import wraps, partial

Event = Dict[str, Any]


# 1. Write ErrorHandler decorator.
# a) nested functions
def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            return f'Error: {e}'

    return wrapper


# b) class
class ErrorHandler:
    def __init__(self, func):
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        try:
            return self.__wrapped__(*args, **kwargs)
        except BaseException as e:
            return f'Error: {e}'


# 2. Decorate this function using decorator

# call without @
def handle1(x, y):
    return x ** y


handle1 = error_handler(handle1)


def handle2(x, y):
    return x - y


handle2 = ErrorHandler(handle2)


# call with @
@error_handler
def handle3(x, y):
    return x / y


@ErrorHandler
def handle4(x, y):
    return x / y


# 3. Show how it works
print(handle1(1, 'hkghkj'))
print(handle2(1, 'gfhjg'))
print(handle3(1, 0))
print(handle4(1, 0))


# 4. Add possibility to use decorator with or without parameter
# a. error_handler - function
def error_handler_param(func=None, *, exception=BaseException):
    if func is None:
        return partial(error_handler_param, exception=exception)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exception as e:
            return f'Error: {e}'

    return wrapper


# without parameters:
@error_handler_param
def handle4(x, y):
    return x / y


print(handle4(3, 'hjkhj'))


# with parameters:
@error_handler_param(exception=ZeroDivisionError)
def handle4(x, y):
    return x / y


print(handle4(3, 0))


# b. ErrorHandler -- class
class ErrorHandlerParam:

    def _set_exception(self, exception):
        self.exception = exception

    def __new__(cls, func=None, exception=BaseException):
        if func is None:
            return partial(cls.__new__, cls, exception=exception)
        instance = super().__new__(cls)
        instance.__init__(func)
        instance.exception = exception
        return instance

    def __init__(self, func):
        wraps(func)(self)
        self.set_exception = self._set_exception

    def __call__(self, *args, **kwargs):
        try:
            return self.__wrapped__(*args, **kwargs)
        except self.exception as e:
            return f'Error: {e}'


# without parameters:
@ErrorHandlerParam
def handle7(x, y):
    return x / y


print(handle7(3, 'ghjghj'))


# with parameters:
@ErrorHandlerParam(exception=ZeroDivisionError)
def handle8(x, y):
    return x / y


print(handle8(3, 0))
