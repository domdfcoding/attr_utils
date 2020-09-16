#!/usr/bin/env python3
#
#  autoattrs.py
"""
A Sphinx directive for documenting `attrs <https://www.attrs.org/>`_ classes.

Provides the :rst:dir:`autoattrs` directive to document a :class:`typing.NamedTuple`.
It behaves much like :rst:dir:`autoclass` and :rst:dir:`autofunction`.

The :rst:dir:`autoattrs` directive can be used directly or as part of :rst:dir:`automodule`.

.. versionadded:: 0.1.0
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
#  Parts based on https://github.com/sphinx-doc/sphinx
#  |  Copyright (c) 2007-2020 by the Sphinx team (see AUTHORS file).
#  |  BSD Licensed
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are
#  |  met:
#  |
#  |  * Redistributions of source code must retain the above copyright
#  |   notice, this list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright
#  |   notice, this list of conditions and the following disclaimer in the
#  |   documentation and/or other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  |  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  |  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  |  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  |  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  |  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  |  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  |  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  |  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from typing import Any, Dict, Optional

# 3rd party
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter
from sphinx_toolbox import __version__
from sphinx_toolbox.more_autodoc.utils import unknown_module_warning

# this package
from attr_utils.docstrings import add_attrs_doc

__all__ = ["AttrsDocumenter", "setup"]


class AttrsDocumenter(ClassDocumenter):
	r"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter`
	for documenting `attrs <https://www.attrs.org/>`__ classes.

	.. versionadded:: 0.1.0
	"""

	objtype = "attrs"
	directivetype = "class"
	priority = ClassDocumenter.priority + 1

	@classmethod
	def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
		"""
		Called to see if a member can be documented by this documenter.

		:param member:
		:param membername:
		:param isattr:
		:param parent:
		"""

		return hasattr(member, "__attrs_attrs__")

	def import_object(self, raiseerror: bool = False) -> bool:
		"""
		Import the object given by ``self.modname`` and ``self.objpath`` and set
		it as ``self.object``.

		If the object is an `attrs <https://www.attrs.org/>`__ class
		:func:`attr_utils.docstrings.add_attrs_doc` will be called.

		:param raiseerror:

		:return: :py:obj:`True` if successful, :py:obj:`False` if an error occurred.
		"""

		ret = super().import_object(raiseerror)
		if hasattr(self.object, "__attrs_attrs__"):
			self.object = add_attrs_doc(self.object)

		return ret

	def generate(
			self,
			more_content: Optional[Any] = None,
			real_modname: Optional[str] = None,
			check_module: bool = False,
			all_members: bool = False,
			) -> None:
		"""
		Generate reST for the object given by ``self.name``, and possibly for its members.

		:param more_content: Additional content to include in the reST output.
		:param real_modname: Module name to use to find attribute documentation.
		:param check_module: If :py:obj:`True`, only generate if the object is defined
			in the module name it is imported from.
		:param all_members: If :py:obj:`True`, document all members.
		"""

		if not self.parse_name():  # pragma: no cover
			# need a module to import
			unknown_module_warning(self)
			return None

		# now, import the module and get object to document
		if not self.import_object():
			return None  # pragma: no cover

		return super().generate(
				more_content=more_content,
				real_modname=real_modname,
				check_module=check_module,
				all_members=all_members,
				)


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup :mod:`attr_utils.autoattrs`.

	:param app:

	.. versionadded:: 0.1.0
	"""

	app.add_autodocumenter(AttrsDocumenter)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}
