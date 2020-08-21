#!/usr/bin/env python
#
#  autodoc_typehints.py
"""
Extension to `sphinx-autodoc-typehints <sphinx-autodoc-typehints>`_ to populate ``__init__.__annotations__`` for
`attrs <https://github.com/python-attrs/attrs>`_ classes.

Use this extension in your Sphinx ``conf.py`` file instead of ``sphinx-autodoc-typehints``.
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
#  Based on https://github.com/agronholm/sphinx-autodoc-typehints
#  Copyright (c) Alex Grönholm
#  MIT Licensed
#

# stdlib
import inspect
from typing import AnyStr, TypeVar

# 3rd party
from sphinx.util import logging
from sphinx_autodoc_typehints import (
		builder_ready,
		get_all_type_hints,
		get_annotation_args,
		get_annotation_class_name,
		get_annotation_module,
		process_signature
		)

# this package
from attr_utils.annotations import add_init_annotations

logger = logging.getLogger(__name__)
pydata_annotations = {
		'Any',
		'AnyStr',
		'Callable',
		'ClassVar',
		'Literal',
		'NoReturn',
		'Optional',
		'Tuple',
		'Union',
		}


def format_annotation(annotation, fully_qualified: bool = False) -> str:
	# Special cases
	if annotation is None or annotation is type(None):  # noqa: E721
		return ':py:obj:`None`'
	elif annotation is Ellipsis:
		return '...'

	# Type variables are also handled specially
	try:
		if isinstance(annotation, TypeVar) and annotation is not AnyStr:  # type: ignore
			return f"\\:py:data:`{annotation!r}`"
	except TypeError:
		pass

	try:
		module = get_annotation_module(annotation)
		class_name = get_annotation_class_name(annotation, module)
		args = get_annotation_args(annotation, module, class_name)
	except ValueError:
		return str(annotation)

	# Redirect all typing_extensions types to the stdlib typing module
	if module == 'typing_extensions':
		module = 'typing'

	full_name = (module + '.' + class_name) if module != 'builtins' else class_name
	prefix = '' if fully_qualified or full_name == class_name else '~'
	role = 'data' if class_name in pydata_annotations else 'class'
	args_format = '\\[{}]'
	formatted_args = ''

	# Some types require special handling
	if full_name == 'typing.NewType':
		args_format = f'\\(:py:data:`~{annotation.__name__}`, {{}})'
		role = 'func'
	elif full_name == 'typing.Union' and len(args) == 2 and type(None) in args:
		full_name = 'typing.Optional'
		args = tuple(x for x in args if x is not type(None))  # noqa: E721
	elif full_name == 'typing.Callable' and args and args[0] is not ...:
		formatted_args = '\\[\\[' + ', '.join(format_annotation(arg) for arg in args[:-1]) + ']'
		formatted_args += ', ' + format_annotation(args[-1]) + ']'
	elif full_name == 'typing.Literal':
		formatted_args = '\\[' + ', '.join(repr(arg) for arg in args) + ']'

	if args and not formatted_args:
		formatted_args = args_format.format(', '.join(format_annotation(arg, fully_qualified) for arg in args))

	return ':py:{role}:`{prefix}{full_name}`{formatted_args}'.format(
			role=role, prefix=prefix, full_name=full_name, formatted_args=formatted_args
			)


def process_docstring(app, what, name, obj, options, lines):
	original_obj = obj
	if isinstance(obj, property):
		obj = obj.fget

	if callable(obj):

		if inspect.isclass(obj):
			obj = add_init_annotations(obj)

			obj = getattr(obj, '__init__')

		obj = inspect.unwrap(obj)
		type_hints = get_all_type_hints(obj, name)

		for argname, annotation in type_hints.items():
			if argname == 'return':
				continue  # this is handled separately later
			if argname.endswith('_'):
				argname = '{}\\_'.format(argname[:-1])

			formatted_annotation = format_annotation(
					annotation, fully_qualified=app.config.typehints_fully_qualified
					)

			searchfor = [f':{field} {argname}:' for field in ('param', 'parameter', 'arg', 'argument')]
			insert_index = None

			for i, line in enumerate(lines):
				if any(line.startswith(search_string) for search_string in searchfor):
					insert_index = i
					break

			if insert_index is None and app.config.always_document_param_types:
				lines.append(f':param {argname}:')
				insert_index = len(lines)

			if insert_index is not None:
				lines.insert(insert_index, f':type {argname}: {formatted_annotation}')

		if 'return' in type_hints and not inspect.isclass(original_obj):
			# This avoids adding a return type for data class __init__ methods
			if what == 'method' and name.endswith('.__init__'):
				return

			formatted_annotation = format_annotation(
					type_hints['return'], fully_qualified=app.config.typehints_fully_qualified
					)

			insert_index = len(lines)
			for i, line in enumerate(lines):
				if line.startswith(':rtype:'):
					insert_index = None
					break
				elif line.startswith(':return:') or line.startswith(':returns:'):
					insert_index = i

			if insert_index is not None and app.config.typehints_document_rtype:
				if insert_index == len(lines):
					# Ensure that :rtype: doesn't get joined with a paragraph of text, which
					# prevents it being interpreted.
					lines.append('')
					insert_index += 1

				lines.insert(insert_index, f':rtype: {formatted_annotation}')


def setup(app):
	app.add_config_value('set_type_checking_flag', False, 'html')
	app.add_config_value('always_document_param_types', False, 'html')
	app.add_config_value('typehints_fully_qualified', False, 'env')
	app.add_config_value('typehints_document_rtype', True, 'env')
	app.connect('builder-inited', builder_ready)
	app.connect('autodoc-process-signature', process_signature)
	app.connect('autodoc-process-docstring', process_docstring)
	return dict(parallel_read_safe=True)
