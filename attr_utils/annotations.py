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


Examples
---------------

**Library Usage:**

.. code-block:: python

	def my_converter(arg: List[Dict[str, Any]]):
		return arg


	def untyped_converter(arg):
		return arg


	@attr.s
	class SomeClass:
		a_string: str = attr.ib(converter=str)
		custom_converter: Any = attr.ib(converter=my_converter)
		untyped: Tuple[str, int, float] = attr.ib(converter=untyped_converter)
		annotated: List[str] = attr.ib(converter=list, metadata={"annotation": Sequence[str]})

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

The ``parse_occupations`` looks like:

	.. literalinclude:: ../../attr_utils/annotations.py
		:tab-width: 4
		:pyobject: parse_occupations

The Sphinx output looks like:

	.. autoclass:: attr_utils.annotations.AttrsClass
		:members:
		:no-special-members:


API Reference
---------------

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

# stdlib
import inspect
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Type, Union

# 3rd party
import attr
from typing_inspect import get_origin  # type: ignore

# this package
from attr_utils import __version__

if TYPE_CHECKING:
	# 3rd party
	from sphinx.application import Sphinx

__all__ = ["add_init_annotations", "attrib", "attr_docstring_hook", "setup"]


def add_init_annotations(obj: Callable) -> Callable:
	"""
	Add type annotations to the ``__init__`` of an attrs_ class.

	.. _attrs: https://www.attrs.org/en/stable/
	"""

	if not hasattr(obj, "__attrs_attrs__"):
		return obj

	annotations: Dict[str, Optional[Type]] = {"return": None}

	attrs = getattr(obj, "__attrs_attrs__")

	for a in attrs:
		arg_name = a.name.lstrip("_")

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
					if arg_type is inspect.Signature.empty:  # type: ignore
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
		repr=True,
		hash=None,
		init=True,
		metadata=None,
		annotation: Union[Type, object] = attr.NOTHING,  # type: ignore
		converter=None,
		factory=None,
		kw_only=False,
		eq=None,
		order=None,
		on_setattr=None,
		):
	"""
	Wrapper around :func:`attr.ib` which supports the ``annotation``
	keyword argument for use by :func:`~.add_init_annotations`.

	:param metadata: The type to add to ``__init__.__annotations__``, if different from
		that the type taken as input to the converter function or the type hint of the attribute.

	See the documentation for :func:`attr.ib` for descriptions of the other arguments.

	.. versionadded:: 0.2.0
	"""

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
			on_setattr=on_setattr,
			)


def attr_docstring_hook(obj: Any) -> Any:
	"""
	Hook for :mod:`sphinx_toolbox.more_autodoc.typehints` to add annotations to the ``__init__`` of
	attrs_ classes.

	.. _attrs: https://www.attrs.org/en/stable/

	:param obj: The object being documented.
	"""  # noqa D400

	if callable(obj):

		if inspect.isclass(obj):
			obj = add_init_annotations(obj)

	return obj


def setup(app: "Sphinx") -> Dict[str, Any]:
	"""
	Sphinx extension to populate ``__init__.__annotations__`` for attrs_ classes.

	.. _attrs: https://www.attrs.org/en/stable/

	:param app:

	:return:
	"""

	# 3rd party
	from sphinx_toolbox.more_autodoc.typehints import docstring_hooks

	docstring_hooks.append((attr_docstring_hook, 50))

	app.setup_extension("sphinx_toolbox.more_autodoc.typehints")

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}


################################
# Demo
################################


def parse_occupations(occupations: Iterable[str]) -> Iterable[str]:  # pragma: no cover
	if isinstance(occupations, str):
		return [x.strip() for x in occupations.split(",")]
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
