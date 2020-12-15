#!/usr/bin/env python
#
#  docstrings.py
"""
Add better docstrings to attrs generated functions.
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
import re
from typing import Optional, Pattern, Type

# 3rd party
from domdf_python_tools.doctools import PYPY, base_new_docstrings, prettify_docstrings
from domdf_python_tools.typing import MethodDescriptorType, MethodWrapperType, WrapperDescriptorType

__all__ = ["add_attrs_doc"]

attrs_docstring = "Automatically created by attrs."
ne_default = "Check equality and either forward a NotImplemented or return the result\n    negated."
attrs_20_1_docstring: Pattern = re.compile(r"^\s*Method generated by attrs for class .*\.\s*")
repr_doc_template = "Return a string representation of the :class:`~.{name}`."
pickle_state_template = "Used for `pickling <https://docs.python.org/3/library/pickle.html>`_.\n\n{doc}"


def add_attrs_doc(obj: Type) -> Type:
	"""
	Add better docstrings to attrs generated functions.

	:param obj: The class to improve the docstrings for.
	"""

	obj = prettify_docstrings(obj)

	new_docstrings = {
			**base_new_docstrings,
			"__repr__": repr_doc_template.format(name=obj.__name__),
			"__setstate__": pickle_state_template.format(doc=attrs_docstring),
			"__getstate__": pickle_state_template.format(doc=attrs_docstring),
			}

	if hasattr(obj, "__ne__"):
		if PYPY or not isinstance(obj.__ne__, (WrapperDescriptorType, MethodDescriptorType, MethodWrapperType)):
			if obj.__ne__.__doc__ is None or obj.__ne__.__doc__.strip() in {object.__ne__.__doc__, ne_default}:
				obj.__ne__.__doc__ = new_docstrings["__ne__"]

	if hasattr(obj, "__repr__"):
		if (
				obj.__repr__.__doc__ is None or obj.__repr__.__doc__.strip() == attrs_docstring
				or attrs_20_1_docstring.match(obj.__repr__.__doc__)
				):
			_new_doc = f"{new_docstrings['__repr__']}"  # \n\n{attrs_docstring}
			obj.__repr__.__doc__ = _new_doc  # prevents strange formatting in pycharm

	for attr_name in new_docstrings:

		if not hasattr(obj, attr_name):
			continue

		attribute = getattr(obj, attr_name)

		if not PYPY and isinstance(attribute, (WrapperDescriptorType, MethodDescriptorType, MethodWrapperType)):
			continue

		if attribute is None:
			continue

		doc: Optional[str] = attribute.__doc__

		if doc is None or doc.strip() == attrs_docstring or attrs_20_1_docstring.match(doc):
			_new_doc = f"{new_docstrings[attr_name]}"  # \n\n{attrs_docstring}
			attribute.__doc__ = _new_doc  # prevents strange formatting in pycharm

	return obj
