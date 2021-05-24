#!/usr/bin/env python
#
#  pprint.py
r"""
Pretty printing functions.

This module monkeypatches `prettyprinter <https://prettyprinter.readthedocs.io>`_
to disable a potentially undesirable behaviour of its singledispatch feature,
where deferred types took precedence over resoled types.

It also changes the pretty print output for an :class:`enum.Enum` to be the same as the
:class:`~enum.Enum`\'s ``__repr__``.

.. extras-require:: pprint
	:pyproject:

.. autosummary-widths:: 4/16

.. automodulesumm:: attr_utils.pprinter
	:autosummary-sections: Classes ;; Data

.. autosummary-widths:: 7/16
	:html: 3/10

.. automodulesumm:: attr_utils.pprinter
	:autosummary-sections: Functions
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import Any, Callable, Optional, Type, TypeVar, Union

# 3rd party
import attr
from typing_extensions import Protocol, runtime_checkable

try:
	# 3rd party
	import prettyprinter  # type: ignore  # nodep
	from prettyprinter.prettyprinter import _BASE_DISPATCH, pretty_dispatch  # type: ignore  # nodep
except ImportError as e:  # pragma: no cover
	exc = type(e)(f"Could not import 'prettyprinter'. Perhaps you need to install 'attr_utils[pprint]'?\n\n{e}")
	raise exc.with_traceback(e.__traceback__) from None

__all__ = ["pretty_repr", "register_pretty", "PrettyFormatter", "_PF"]

_T = TypeVar("_T")
_PF = TypeVar("_PF", bound="PrettyFormatter")

prettyprinter.install_extras(["attrs"])


@runtime_checkable
class PrettyFormatter(Protocol):
	"""
	:class:`typing.Protocol` representing the pretty formatting functions decorated by :func:`register_pretty`.

	.. versionadded:: 0.6.0
	.. latex:vspace:: 10px
	"""

	def __call__(self, value: Any, ctx: Any) -> str:
		"""
		Call the function.

		:param value: The value to pretty print.
		:param ctx: The context.
		"""

		raise NotImplementedError


def register_pretty(
		type: Union[Type, str, None] = None,  # noqa: A002  # pylint: disable=redefined-builtin
		predicate: Optional[Callable[[Any], bool]] = None,
		) -> Callable[[_PF], _PF]:
	"""
	Returns a decorator that registers the decorated function
	as the pretty printer for instances of ``type``.

	:param type: The type to register the pretty printer for,
		or a :class:`str` to indicate the module and name, e.g. ``'collections.Counter'``.

	:param predicate: A predicate function that takes one argument
		and returns a boolean indicating if the value should be handled
		by the registered pretty printer.

	Only one of ``type`` and ``predicate`` may be supplied,
	and therefore ``predicate`` will only be called for unregistered types.

	:rtype:

	Here's an example of the pretty printer for :class:`collections.OrderedDict`:

	.. code-block:: python

		from collections import OrderedDict
		from attr_utils.pprinter import register_pretty
		from prettyprinter import pretty_call

		@register_pretty(OrderedDict)
		def pretty_orderreddict(value, ctx):
			return pretty_call(ctx, OrderedDict, list(value.items()))
	"""  # noqa: D400

	return prettyprinter.prettyprinter.register_pretty(type=type, predicate=predicate)


def is_registered(
		type,  # noqa: A002  # pylint: disable=redefined-builtin
		*,
		check_superclasses: bool = False,
		check_deferred: bool = True,
		register_deferred: bool = True,
		):
	if not check_deferred and register_deferred:
		raise ValueError("register_deferred may not be True when check_deferred is False")

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
	Add a pretty-printing ``__repr__`` function to the decorated attrs class.

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
