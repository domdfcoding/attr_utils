#  Based on https://github.com/agronholm/sphinx-autodoc-typehints
#  Copyright (c) Alex Grönholm
#  MIT Licensed
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

import typing
from mailbox import Mailbox
from typing import Callable, Union

try:
    from dataclasses import dataclass
except ImportError:
    def dataclass(cls):
        return cls


def get_local_function():
    def wrapper(self) -> str:
        """
        Wrapper
        """
    return wrapper


class Class:
    """
    Initializer docstring.

    :param x: foo
    :param y: bar
    :param z: baz
    """

    def __init__(self, x: bool, y: int, z: typing.Optional[str] = None) -> None:
        pass

    def a_method(self, x: bool, y: int, z: typing.Optional[str] = None) -> str:
        """
        Method docstring.

        :param x: foo
        :param y: bar
        :param z: baz
        """

    def _private_method(self, x: str) -> str:
        """
        Private method docstring.

        :param x: foo
        """

    def __dunder_method(self, x: str) -> str:
        """
        Dunder method docstring.

        :param x: foo
        """

    def __magic_custom_method__(self, x: str) -> str:
        """
        Magic dunder method docstring.

        :param x: foo
        """

    @classmethod
    def a_classmethod(cls, x: bool, y: int, z: typing.Optional[str] = None) -> str:
        """
        Classmethod docstring.

        :param x: foo
        :param y: bar
        :param z: baz
        """

    @staticmethod
    def a_staticmethod(x: bool, y: int, z: typing.Optional[str] = None) -> str:
        """
        Staticmethod docstring.

        :param x: foo
        :param y: bar
        :param z: baz
        """

    @property
    def a_property(self) -> str:
        """
        Property docstring
        """

    class InnerClass:
        """
        Inner class.
        """

        def inner_method(self, x: bool) -> str:
            """
            Inner method.

            :param x: foo
            """

        def __dunder_inner_method(self, x: bool) -> str:
            """
            Dunder inner method.

            :param x: foo
            """

    locally_defined_callable_field = get_local_function()


class DummyException(Exception):
    """
    Exception docstring

    :param message: blah
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


def function(x: bool, y: int, z_: typing.Optional[str] = None) -> str:
    """
    Function docstring.

    :param x: foo
    :param y: bar
    :param z\\_: baz
    :return: something
    :rtype: bytes
    """


def function_with_escaped_default(x: str = '\b'):
    """
    Function docstring.

    :param x: foo
    """


def function_with_unresolvable_annotation(x: 'a.b.c'):  # noqa: F821
    """
    Function docstring.

    :arg x: foo
    """


def function_with_typehint_comment(
    x,  # type: int
    y   # type: str
):
    # type: (...) -> None
    """
    Function docstring.

    :parameter x: foo
    :param y: bar
    """


class ClassWithTypehints(object):
    """
    Class docstring.

    :param x: foo
    """

    def __init__(
        self,
        x  # type: int
    ):
        # type: (...) -> None
        pass

    def foo(
        self,
        x  # type: str
    ):
        # type: (...) -> int
        """
        Method docstring.

        :arg x: foo
        """
        return 42


def function_with_typehint_comment_not_inline(x=None, *y, z, **kwargs):
    # type: (Union[str, bytes], *str, bytes, **int) -> None
    """
    Function docstring.

    :arg x: foo
    :argument y: bar
    :parameter z: baz
    :parameter kwargs: some kwargs
    """


class ClassWithTypehintsNotInline(object):
    """
    Class docstring.

    :param x: foo
    """

    def __init__(self, x=None):
        # type: (Callable[[int, bytes], int]) -> None
        pass

    def foo(self, x=1):
        # type: (Callable[[int, bytes], int]) -> int
        """
        Method docstring.

        :param x: foo
        """
        return x(1, b'')

    @classmethod
    def mk(cls, x=None):
        # type: (Callable[[int, bytes], int]) -> ClassWithTypehintsNotInline
        """
        Method docstring.

        :param x: foo
        """
        return cls(x)


def undocumented_function(x: int) -> str:
    """Hi"""

    return str(x)


@dataclass
class DataClass:
    """Class docstring."""


class Decorator:
    """
    Initializer docstring.

    :param func: function
    """

    def __init__(self, func: Callable[[int, str], str]):
        pass


def mocked_import(x: Mailbox):
    """
    A docstring.

    :param x: function
    """
