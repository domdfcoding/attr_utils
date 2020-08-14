#!/usr/bin/env python
#
#  annotations.py
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
from typing import Any, Callable, Dict, Optional

__all__ = ["add_attrs_doc"]

attrs_docstring = "Automatically created by attrs."
eq_default = "Return self==value."
ne_default = "Check equality and either forward a NotImplemented or return the result\n    negated."
repr_default = {"Return repr(self).", attrs_docstring}


def add_attrs_doc(obj: Callable) -> Callable:
	"""
	Add better docstrings to attrs generated functions.

	:param obj:
	"""

	new_docstrings = {
			"__eq__": "Return ``self == other``.",
			"__ge__": "Return ``self >= other``.",
			"__gt__": "Return ``self > other``.",
			"__lt__": "Return ``self < other``.",
			"__le__": "Return ``self <= other``.",
			"__ne__": "Return ``self != other``.",
			"__repr__": f"Return a string representation of the :class:`~.{obj.__name__}`.",
			}

	new_return_types = {
			"__eq__": bool,
			"__ge__": bool,
			"__gt__": bool,
			"__lt__": bool,
			"__le__": bool,
			"__ne__": bool,
			"__repr__": str,
			}

	if obj.__eq__.__doc__ is None or obj.__eq__.__doc__.strip() == eq_default:
		obj.__eq__.__doc__ = new_docstrings["__eq__"]

	if obj.__ne__.__doc__ is None or obj.__ne__.__doc__.strip() == ne_default:
		obj.__ne__.__doc__ = new_docstrings["__ne__"]

	if hasattr(obj, "__repr__"):
		if obj.__repr__.__doc__ is None or obj.__repr__.__doc__.strip() in repr_default:
			obj.__repr__.__doc__ = new_docstrings["__repr__"]

	for attribute in new_docstrings:
		doc: Optional[str] = getattr(obj, attribute).__doc__
		if doc is None or doc.strip() == attrs_docstring:
			getattr(obj, attribute).__doc__ = new_docstrings[attribute]

	for attribute in new_return_types:
		annotations: Dict = getattr(getattr(obj, attribute), "__annotations__", {})
		if "return" not in annotations or annotations["return"] is Any:
			annotations["return"] = new_return_types[attribute]

		try:
			getattr(obj, attribute).__annotations__ = annotations
		except AttributeError:  # pragma: no cover
			pass

	return obj
