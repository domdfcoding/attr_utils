#!/usr/bin/env python
#
#  annotations.py
"""
Add type annotations to the ``__init__`` of an attrs_ class.

Since :pull:`363 <python-attrs/attrs>` attrs has
populated the ``__init__.__annotations__`` based on the types of attributes.
However, annotations were deliberately omitted when converter functions were used.
This module attempts to generate the annotations for use in Sphinx documentation,
even when converter functions *are* used, based on the following assumptions:

* If the converter function is a Python ``type``, such as :class:`str`, :class:`int`,
  or :class:`list`, the type annotation will be that type.
  If the converter and the type annotation refer to the same type
  (e.g. :class:`list` and :class:`typing.List`) the type annotation will be used.

* If the converter function has an annotation for its first argument, that annotation is used.

* If the converter function is not annotated, the type of the attribute will be used.

The annotation can also be provided via the ``'annotation'`` key in the
`metadata dict <https://www.attrs.org/en/stable/examples.html#metadata>`_.
If you prefer you can instead provide this as a keyword argument to :func:`~.attrib`
which will construct the metadata dict and call :func:`attr.ib` for you.

.. _attrs: https://www.attrs.org/en/stable/

.. versionchanged:: 0.2.0

	Improved support for container types.


.. attention::

	Due to changes in the :mod:`typing` module :mod:`~attr_utils.annotations`
	is only officially supported on Python 3.7 and above.

Examples
---------------

**Library Usage:**

.. code-block:: python
	:linenos:

	def my_converter(arg: List[Dict[str, Any]]):
		return arg


	def untyped_converter(arg):
		return arg


	@attr.s
	class SomeClass:
		a_string: str = attr.ib(converter=str)
		custom_converter: Any = attr.ib(converter=my_converter)
		untyped: Tuple[str, int, float] = attr.ib(converter=untyped_converter)
		annotated: List[str] = attr.ib(
			converter=list,
			metadata={"annotation": Sequence[str]},
		)

	add_attrs_annotations(SomeClass)

	print(SomeClass.__init__.__annotations__)
	# {
	#	'return': None,
	#	'a_string': <class 'str'>,
	#	'custom_converter': typing.List[typing.Dict[str, typing.Any]],
	#	'untyped': typing.Tuple[str, int, float],
	#	}

**Sphinx documentation**:

.. literalinclude:: ../../attr_utils/annotations.py
	:tab-width: 4
	:pyobject: AttrsClass

The ``parse_occupations`` function looks like:

.. literalinclude:: ../../attr_utils/annotations.py
	:tab-width: 4
	:pyobject: parse_occupations

The Sphinx output looks like:

	.. autoclass:: attr_utils.annotations.AttrsClass
		:members:
		:no-special-members:


API Reference
---------------

"""  # noqa: RST399
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

# stdlib
import inspect
import sys
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Type, TypeVar, Union, cast

# 3rd party
import attr

# this package
import attr_utils

if sys.version_info > (3, 7):  # pragma: no cover (<py37)
	# 3rd party
	from typing_extensions import get_origin
else:  # pragma: no cover (py37+)
	# 3rd party
	from typing_inspect import get_origin  # type: ignore

if TYPE_CHECKING or attr_utils._docs:
	# 3rd party
	from sphinx.application import Sphinx
	from sphinx_toolbox.utils import SphinxExtMetadata

__all__ = ["attrib", "_A", "_C", "add_init_annotations", "attr_docstring_hook", "setup"]

_A = TypeVar("_A", bound=Any)
_C = TypeVar("_C", bound=Callable)


def add_init_annotations(obj: _C) -> _C:
	"""
	Add type annotations to the ``__init__`` method of an attrs_ class.

	.. _attrs: https://www.attrs.org/en/stable/
	"""

	if not attr.has(obj):  # type: ignore
		return obj

	annotations: Dict[str, Optional[Type]] = {"return": None}

	attrs = attr.fields(obj)  # type: ignore

	for a in attrs:
		arg_name = a.name.lstrip('_')

		if a.init is True and a.type is not None:
			if a.converter is None:
				annotations[arg_name] = a.type
			else:

				if "annotation" in a.metadata:
					annotations[arg_name] = a.metadata["annotation"]

				elif isinstance(a.converter, type):
					if a.converter is get_origin(a.type):
						annotations[arg_name] = a.type
					else:
						annotations[arg_name] = a.converter

				else:
					signature = inspect.signature(a.converter)
					arg_type = next(iter(signature.parameters.items()))[1].annotation
					if arg_type is inspect.Signature.empty:
						annotations[arg_name] = a.type
					else:
						annotations[arg_name] = arg_type

	if hasattr(obj.__init__, "__annotations__"):  # type: ignore
		obj.__init__.__annotations__.update(annotations)  # type: ignore
	else:  # pragma: no cover
		obj.__init__.__annotations__ = annotations  # type: ignore

	return obj


def attrib(
		default=attr.NOTHING,
		validator=None,
		repr: bool = True,  # noqa: A002  # pylint: disable=redefined-builtin
		hash=None,  # noqa: A002  # pylint: disable=redefined-builtin
		init=True,
		metadata=None,
		annotation: Union[Type, object] = attr.NOTHING,
		converter=None,
		factory=None,
		kw_only: bool = False,
		eq=None,
		order=None,
		**kwargs,
		):
	r"""
	Wrapper around :func:`attr.ib` which supports the ``annotation``
	keyword argument for use by :func:`~.add_init_annotations`.

	.. versionadded:: 0.2.0

	:param default:
	:param validator:
	:param repr:
	:param hash:
	:param init:
	:param metadata:
	:param annotation: The type to add to ``__init__.__annotations__``, if different to
		that the type taken as input to the converter function or the type hint of the attribute.
	:param converter:
	:param factory:
	:param kw_only:
	:param eq:
	:param order:

	See the documentation for :func:`attr.ib` for descriptions of the other arguments.
	"""  # noqa: D400

	if annotation is not attr.NOTHING:
		if metadata is None:
			metadata = {}

		metadata["annotation"] = annotation

	return attr.ib(
			default=default,
			validator=validator,
			repr=repr,
			hash=hash,
			init=init,
			metadata=metadata,
			converter=converter,
			factory=factory,
			kw_only=kw_only,
			eq=eq,
			order=order,
			**kwargs,
			)


def attr_docstring_hook(obj: _A) -> _A:
	"""
	Hook for :mod:`sphinx_toolbox.more_autodoc.typehints` to add annotations to the ``__init__`` method
	of attrs_ classes.

	.. _attrs: https://www.attrs.org/en/stable/

	:param obj: The object being documented.
	"""  # noqa: D400

	if callable(obj):

		if inspect.isclass(obj):
			obj = cast(_A, add_init_annotations(obj))

	return obj


def setup(app: "Sphinx") -> "SphinxExtMetadata":
	"""
	Sphinx extension to populate ``__init__.__annotations__`` for attrs_ classes.

	.. _attrs: https://www.attrs.org/en/stable/

	:param app:
	"""

	# 3rd party
	from sphinx_toolbox.more_autodoc.typehints import docstring_hooks  # nodep

	docstring_hooks.append((attr_docstring_hook, 50))

	app.setup_extension("sphinx_toolbox.more_autodoc.typehints")

	return {
			"version": attr_utils.__version__,
			"parallel_read_safe": True,
			}


################################
# Demo
################################


def parse_occupations(  # pragma: no cover
		occupations: Iterable[str],
		) -> Iterable[str]:

	if isinstance(occupations, str):
		return [x.strip() for x in occupations.split(',')]
	else:
		return [str(x) for x in occupations]


@attr.s
class AttrsClass:
	"""
	Example of using :func:`~.add_init_annotations` for attrs_ classes with Sphinx documentation.

	.. _attrs: https://www.attrs.org/en/stable/

	:param name: The name of the person.
	:param age: The age of the person.
	:param occupations: The occupation(s) of the person.
	"""

	name: str = attr.ib(converter=str)
	age: int = attr.ib(converter=int)
	occupations: List[str] = attr.ib(converter=parse_occupations)
