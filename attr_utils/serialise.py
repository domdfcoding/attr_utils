#!/usr/bin/env python
#
#  annotations.py
"""
Add serialisation and deserialisation capability to attrs_ classes.

.. _attrs: https://www.attrs.org/en/stable/

Based on `attrs-serde <https://github.com/jondot/attrs-serde>`_.

Example usage
--------------

.. code-block:: python

	>>> import attr
	>>> from attr_utils.serialise import serde

	>>> person_dict = {"contact": {"personal": {"name": "John"}, "phone": "555-112233"}}

	>>> name_path = ["contact", "personal", "name"]
	>>> phone_path = ["contact", "phone"]

	>>> @serde
	... @attr.s
	... class Person(object):
	... 	name = attr.ib(metadata={"to": name_path, "from": name_path})
	... 	phone = attr.ib(metadata={"to": phone_path, "from": phone_path})

	>>> p = Person.from_dict(person_dict)
	Person(name=John phone=555-112233)

	>>> p.to_dict
	{"contact": {"personal": {"name": "John"}, "phone": "555-112233"}}


API Reference
---------------
"""

#  From https://github.com/jondot/attrs-serde
#  MIT License
#
#  Copyright (c) 2019 Dotan Nahum
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
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

# stdlib
from typing import TYPE_CHECKING, Any, Callable, Mapping, MutableMapping, Optional, Type, Union, overload

try:
	# 3rd party
	from cytoolz import curried  # type: ignore
except ImportError:
	from toolz import curried  # type: ignore

# 3rd party
from attr import asdict, fields

__all__ = ["serde"]

if TYPE_CHECKING:
	AttrsClass = Any
else:
	# this package
	from attr_utils.utils import AttrsClass


@overload
def serde(
		cls: Type,
		from_key: str = ...,
		to_key: str = ...,
		) -> Type[AttrsClass]: ...


@overload
def serde(
		cls: None = None,
		from_key: str = ...,
		to_key: str = ...,
		) -> Callable[[Type[AttrsClass]], Type[AttrsClass]]: ...


def serde(
		cls: Optional[Type[AttrsClass]] = None,
		from_key: str = "from",
		to_key: str = "to",
		) -> Union[Type[AttrsClass], Callable[[Type[AttrsClass]], Type[AttrsClass]]]:
	r"""
	Decorator to add serialisation and deserialisation capabilities to attrs classes.

	The keys used in the dictionary output, and used when creating the class from a dictionary,
	can be controlled using the ``metadata`` argument in :func:`attr.ib`:

	.. code-block::

		from attr_utils.serialize import serde
		import attr

		@serde
		@attr.s
		class Person(object):
			name = attr.ib(metadata={"to": name_path, "from": name_path})
			phone = attr.ib(metadata={"to": phone_path, "from": phone_path})

	The names of the keys given in the ``metadata`` argument can be controlled with the
	``from_key`` and ``to_key`` arguments:

	.. code-block::

		from attr_utils.serialize import serde
		import attr

		@serde(from_key="get", to_key="set")
		@attr.s
		class Person(object):
			name = attr.ib(metadata={"get": name_path, "set": name_path})
			phone = attr.ib(metadata={"get": phone_path, "set": phone_path})


	This may be required when using other extensions to attrs.


	:param cls: The attrs class to add the methods to.
	:param from_key:
	:param to_key:

	:rtype:

	.. latex:vspace:: 20px

	Classes decorated with :deco:`~attr_utils.serialise.serde` will have two new methods added:

	.. py:classmethod:: from_dict(d)

		Construct an instance of the class from a dictionary.

		:param d: The dictionary.
		:type d: :class:`~typing.Mapping`\[:class:`str`, :py:obj:`~typing.Any`\]

	.. py:method:: to_dict(convert_values=False):

		Returns a dictionary containing the contents of the class.

		:param convert_values: Recurse into other attrs classes, and convert tuples, sets etc.
			into lists. This may be required to later construct a new class from the
			dictionary if the class uses complex converter functions.
		:type convert_values: :class:`bool`

		:rtype: :class:`~typing.MutableMapping`\[:class:`str`, :py:obj:`~typing.Any`\]

		.. versionchanged:: 0.5.0

			By default values are left unchanged. In version 0.4.0 these were converted
			to basic Python types, which may be undesirable. The original behaviour can be
			restored using the ``convert_values`` parameter.

	"""

	def serde_with_class(cls: Type[AttrsClass]) -> Type[AttrsClass]:

		def from_dict(cls, d: Mapping[str, Any]):
			from_fields = list(map(lambda a: (a, curried.get_in([from_key], a.metadata, [a.name])), fields(cls)))

			return cls(**dict(map(
					lambda f: (f[0].name, curried.get_in(f[1], d, f[0].default)),
					from_fields,
					)))

		def to_dict(self, convert_values: bool = False) -> MutableMapping[str, Any]:
			to_fields = curried.pipe(
					fields(self.__class__),
					curried.map(lambda a: (a, curried.get_in([to_key], a.metadata))),
					curried.filter(lambda f: f[1]),
					list,
					)

			if convert_values:
				d = asdict(self)
			else:
				d = {a.name: getattr(self, a.name) for a in fields(self.__class__)}

			if not to_fields:
				return d

			return curried.reduce(
					lambda acc, f: curried.update_in(acc, f[1], lambda _: d[f[0].name]),
					to_fields,
					{},
					)

		from_dict.__doc__ = f"""
		Construct an instance of :class:`~.{cls.__name__}` from a dictionary.

		:param d: The dictionary.
		"""
		from_dict.__qualname__ = f"{cls.__name__}.from_dict"
		from_dict.__module__ = cls.__module__
		cls.from_dict = classmethod(from_dict)

		to_dict.__doc__ = f"""
Returns a dictionary containing the contents of the :class:`~.{cls.__name__}` object.

:param convert_values: Recursively convert values into dictionaries, lists etc. as appropriate.
"""
		to_dict.__qualname__ = f"{cls.__name__}.to_dict"
		to_dict.__module__ = cls.__module__
		cls.to_dict = to_dict

		return cls

	if cls is not None:
		return serde_with_class(cls)
	else:
		return serde_with_class
