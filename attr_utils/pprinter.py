#!/usr/bin/env python
#
#  pprint.py
r"""
Pretty printing functions.

This module monkeypatches `PrettyPrinter <https://prettyprinter.readthedocs.io>`_
to disable a potentially undesirable behaviour of its singledispatch feature,
where deferred types took precedence over resoled types.

It also changes the pretty print output for an :class:`enum.Enum` to be the same as the
:class:`~enum.Enum`\'s ``__repr__``.

The following functions are available:

"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  Based on https://prettyprinter.readthedocs.io
#  Copyright © 2017, Tommi Kaikkonen.
#

# stdlib
import enum
import sys
from typing import Type, TypeVar

# 3rd party
import attr
import prettyprinter  # type: ignore
from prettyprinter.prettyprinter import _BASE_DISPATCH, pretty_dispatch, register_pretty  # type: ignore

__all__ = ["pretty_enum", "pretty_repr", "register_pretty"]

_T = TypeVar("_T")

prettyprinter.install_extras(["attrs"])


def is_registered(type, *, check_superclasses=False, check_deferred=True, register_deferred=True):
	if not check_deferred and register_deferred:
		raise ValueError('register_deferred may not be True when check_deferred is False')

	if type in pretty_dispatch.registry:
		return True

	if not check_superclasses:
		return False

	return pretty_dispatch.dispatch(type) is not _BASE_DISPATCH


# Resolve deferred names and prevent them being used again.
prettyprinter.is_registered(type(_T), check_superclasses=True, check_deferred=True, register_deferred=True)
prettyprinter.is_registered = is_registered
sys.modules["prettyprinter.prettyprinter"].is_registered = is_registered  # type: ignore


@register_pretty(enum.EnumMeta)
@register_pretty(enum.Enum)
@register_pretty(enum.IntEnum)
@register_pretty(enum.Flag)
@register_pretty(enum.IntFlag)
def pretty_enum(value, ctx) -> str:
	r"""
	Pretty-prints the given :class:`~enum.Enum`.
	"""

	return repr(value)


def pretty_repr(obj: Type):
	"""
	Add a pretty-printed ``__repr__`` function to the decorated attrs class.

	.. code-block:: python

		>>> import attr
		>>> from attr_utils.pprinter import pretty_repr

		>>> @pretty_repr
		... @attr.s
		... class Person(object):
		... 	name = attr.ib()

		>>> repr(Person(name="Bob"))
		Person(name='Bob')

	:param obj:
	"""

	if attr.has(obj):

		def __repr__(self) -> str:
			return prettyprinter.pformat(self)

		__repr__.__doc__ = f"Return a string representation of the :class:`~.{obj.__name__}`."

		obj.__repr__ = __repr__  # type: ignore
		obj.__repr__.__qualname__ = f"{obj.__name__}.__repr__"
		obj.__repr__.__module__ = obj.__module__

	return obj
