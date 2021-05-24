#!/usr/bin/env python3
#
#  autoattrs.py
"""
Sphinx directive for documenting attrs_ classes.

.. _attrs: https://www.attrs.org/en/stable/

.. versionadded:: 0.1.0


.. attention::

	Due to changes in the :mod:`typing` module :mod:`~attr_utils.autoattrs`
	is only officially supported on Python 3.7 and above.

.. extras-require:: sphinx
	:pyproject:


.. rst:directive:: autoattrs

	Autodoc directive to document an `attrs <https://www.attrs.org/>`__ class.

	It behaves much like :rst:dir:`autoclass`. It can be used directly or as part of :rst:dir:`automodule`.

	Docstrings for parameters in ``__init__`` can be given in the class docstring or alongside each attribute
	(see :rst:dir:`autoattribute` for the syntax). The second option is recommended as it interacts better
	with other parts of autodoc. However, the class docstring can be used to override the description
	for a given parameter.

	.. rst:directive:option:: no-init-attribs
		:type: flag

		Excludes attributes taken as arguments in ``__init__`` from the output, even if they are documented.

		This may be useful for simple classes where converter functions aren't used.

		This option cannot be used as part of :rst:dir:`automodule`.


.. latex:clearpage::

API Reference
---------------

.. latex:vspace:: -20px
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
from textwrap import dedent
from typing import Any, Dict, List, MutableMapping, Optional, Tuple, Type

# 3rd party
import attr
from sphinx.application import Sphinx  # nodep
from sphinx.ext.autodoc import ClassDocumenter, Documenter  # nodep
from sphinx.pycode import ModuleAnalyzer  # nodep
from sphinx_toolbox import __version__  # nodep
from sphinx_toolbox.more_autosummary import PatchedAutoSummClassDocumenter  # nodep
from sphinx_toolbox.utils import Param, SphinxExtMetadata, flag, parse_parameters, unknown_module_warning  # nodep

# this package
from attr_utils.docstrings import add_attrs_doc
from attr_utils.utils import AttrsClass

__all__ = ["AttrsDocumenter", "setup"]


class AttrsDocumenter(PatchedAutoSummClassDocumenter):
	r"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter`
	for documenting `attrs <https://www.attrs.org/>`__ classes.

	.. versionchanged:: 0.3.0

		* Parameters for ``__init__`` can be documented either in the class docstring
		  or alongside the attribute.
		  The class docstring has priority.
		* Added support for `autodocsumm <https://github.com/Chilipp/autodocsumm>`_.

	.. autosummary-widths:: 29/64
		:html: 4/10
	"""  # noqa: D400

	objtype = "attrs"
	directivetype = "class"
	priority = ClassDocumenter.priority + 1
	option_spec = {
			**PatchedAutoSummClassDocumenter.option_spec,
			"no-init-attribs": flag,
			}
	object: Type[AttrsClass]  # noqa: A003  # pylint: disable=redefined-builtin

	@classmethod
	def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
		"""
		Called to see if a member can be documented by this documenter.

		:param member:
		:param membername:
		:param isattr:
		:param parent:

		:rtype:

		.. latex:clearpage::
		"""

		return attr.has(member) and isinstance(member, type)

	def add_content(self, more_content: Any, no_docstring: bool = False) -> None:  # type: ignore
		"""
		Add extra content (from docstrings, attribute docs etc.), but not the class docstring.

		:param more_content:
		:param no_docstring:
		"""

		Documenter.add_content(self, more_content, True)

		# set sourcename and add content from attribute documentation
		sourcename = self.get_sourcename()

		params, pre_output, post_output = self._get_docstring()

		self.add_line('', sourcename)
		for line in list(self.process_doc([pre_output])):
			self.add_line(line, sourcename)
		self.add_line('', sourcename)

	def _get_docstring(self) -> Tuple[Dict[str, Param], List[str], List[str]]:
		"""
		Returns params, pre_output, post_output.
		"""

		# Size varies depending on docutils config
		tab_size = self.env.app.config.docutils_tab_width

		if self.object.__doc__:
			docstring = dedent(self.object.__doc__).expandtabs(tab_size).split('\n')
		else:
			docstring = []

		return parse_parameters(docstring, tab_size=tab_size)

	def import_object(self, raiseerror: bool = False) -> bool:
		"""
		Import the object given by ``self.modname`` and ``self.objpath`` and set it as ``self.object``.

		If the object is an `attrs <https://www.attrs.org/>`__ class
		:func:`attr_utils.docstrings.add_attrs_doc` will be called.

		:param raiseerror:

		:return: :py:obj:`True` if successful, :py:obj:`False` if an error occurred.
		"""

		ret = super().import_object(raiseerror)

		if attr.has(self.object):
			self.object = add_attrs_doc(self.object)

		return ret

	def sort_members(
			self,
			documenters: List[Tuple[Documenter, bool]],
			order: str,
			) -> List[Tuple[Documenter, bool]]:
		"""
		Sort the given member list and add attribute docstrings to the class docstring.

		:param documenters:
		:param order:
		"""

		# The documenters for the fields and methods, in the desired order
		# The fields will be in bysource order regardless of the order option
		documenters = super().sort_members(documenters, order)

		if hasattr(self, "_docstring_processed"):
			return documenters

		# Mapping of member names to docstrings (as list of strings)
		member_docstrings = {
				k[1]: v
				for k, v in ModuleAnalyzer.for_module(self.object.__module__).find_attr_docs().items()
				}

		# set sourcename and add content from attribute documentation
		sourcename = self.get_sourcename()

		parameter_docs = []
		params, pre_output, post_output = self._get_docstring()
		all_docs = {}

		for field in (a.name for a in attr.fields(self.object) if a.init):
			doc: List[str] = ['']

			# Prefer doc from class docstring
			if field in params:
				doc, arg_type = params.pop(field).values()  # type: ignore

			# Otherwise use attribute docstring
			if not ''.join(doc).strip() and field in member_docstrings:
				doc = member_docstrings[field]

			field_entry = [f":param {field}:", *doc]
			parameter_docs.append(' '.join(field_entry))
			all_docs[field] = ''.join(doc).strip()

		self.add_line('', sourcename)
		for line in list(self.process_doc([[*parameter_docs, '', '', *post_output]])):
			self.add_line(line, sourcename)
		self.add_line('', sourcename)

		self._docstring_processed = True

		if hasattr(self.object, "__slots__"):
			slots_dict: MutableMapping[str, Optional[str]] = {}
			for item in self.object.__slots__:
				if item in all_docs:
					slots_dict[item] = all_docs[item]
				else:
					slots_dict[item] = None

			self.object.__slots__ = slots_dict

		if hasattr(self, "add_autosummary"):
			self.add_autosummary()

		# import functools
		#
		# for documenter in documenters:
		# 	documenter[0].parse_name()
		# 	if documenter[0].objpath[-1] in all_docs:
		# 		def get_doc(encoding: str = None, ignore: int = None, doc: str = '') -> List[List[str]]:
		# 			return [[doc]]
		# 		documenter[0].get_doc = functools.partial(get_doc, doc=all_docs[documenter[0].objpath[-1]])

		return documenters

	def filter_members(
			self,
			members: List[Tuple[str, Any]],
			want_all: bool,
			) -> List[Tuple[str, Any, bool]]:
		"""
		Filter the list of members to always include init attributes unless the
		``:no-init-attribs:`` flag was given.

		:param members:
		:param want_all:
		"""  # noqa: D400

		attrib_names = (a.name for a in attr.fields(self.object) if a.init)

		no_init_attribs = self.options.get("no-init-attribs", False)

		def unskip_attrs(app, what, name, obj, skip, options):
			if skip and not no_init_attribs:
				return not (name in attrib_names)
			elif no_init_attribs and (name in attrib_names):
				return True
			return None

		listener_id = self.env.app.connect("autodoc-skip-member", unskip_attrs)
		members_ = super().filter_members(members, want_all)
		self.env.app.disconnect(listener_id)

		return members_

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

		.. latex:vspace:: -6px
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


def setup(app: Sphinx) -> SphinxExtMetadata:
	"""
	Setup :mod:`attr_utils.autoattrs`.

	:param app:
	"""

	# Hack to get the docutils tab size, as there doesn't appear to be any other way
	app.setup_extension("sphinx_toolbox.tweaks.tabsize")

	app.setup_extension("sphinx_toolbox.more_autosummary")

	app.add_autodocumenter(AttrsDocumenter)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}
