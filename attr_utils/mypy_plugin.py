#!/usr/bin/env python
#
#  mypy_plugin.py
"""
Plugin for `mypy <https://github.com/python/mypy>`_ which adds support for attr_utils.

.. versionadded:: 0.4.0

.. compound::

	To use this plugin, add the following to your
	`mypy configuration file <https://mypy.readthedocs.io/en/stable/config_file.html>`_:

		.. code-block:: ini

			[mypy]
			plugins=attr_utils.mypy_plugin

	See https://mypy.readthedocs.io/en/stable/extending_mypy.html#configuring-mypy-to-use-plugins
	for more information.

.. autosummary-widths:: 7/16
	:html: 2/10

.. automodulesumm:: attr_utils.mypy_plugin
	:autosummary-sections: Classes

.. autosummary-widths:: 1/2
	:html: 4/10

.. automodulesumm:: attr_utils.mypy_plugin
	:autosummary-sections: Functions
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
#  Based on https://github.com/python/mypy/issues/5719
#  and https://gitter.im/python/typing?at=5e078653eac8d1511e737d8c
#
#  Also based on mypy
#  https://github.com/python/mypy
#  Copyright (c) 2015-2019 Jukka Lehtosalo and contributors
#  Licensed under the terms of the MIT license.
#

# stdlib
from typing import Any, Callable, List, MutableMapping, Optional

# 3rd party
from mypy.nodes import (  # nodep
		ARG_OPT,
		ARG_POS,
		MDEF,
		Argument,
		Block,
		ClassDef,
		FuncDef,
		PassStmt,
		SymbolTableNode,
		Var
		)
from mypy.plugin import ClassDefContext, Plugin, SemanticAnalyzerPluginInterface  # nodep
from mypy.plugins.common import add_method_to_class  # nodep
from mypy.semanal_shared import set_callable_name  # nodep
from mypy.types import AnyType, CallableType, Instance, Type, TypeOfAny, TypeType  # nodep
from mypy.typevars import fill_typevars  # nodep
from mypy.util import get_unique_redefinition_name  # nodep
from mypy.version import __version__ as mypy_version  # nodep

__all__ = ["attr_utils_serialise_serde", "AttrUtilsPlugin", "add_classmethod_to_class", "plugin"]

#: Registry mapping decorator full names to the callable that handles the methods added by the decorator.
decorator_registry: MutableMapping[str, Callable[[ClassDefContext], None]] = {}

# ref: https://github.com/python/mypy/pull/11332
_builtins = "builtins" if mypy_version > "0.930" else "__builtins__"


def attr_utils_serialise_serde(cls_def_ctx: ClassDefContext):
	"""
	Handles :func:`attr_utils.serialise.serde`.

	:param cls_def_ctx:
	"""

	info = cls_def_ctx.cls.info

	# https://gitter.im/python/typing?at=5e078653eac8d1511e737d8c
	str_type = cls_def_ctx.api.named_type(f"{_builtins}.str")
	bool_type = cls_def_ctx.api.named_type(f"{_builtins}.bool")
	implicit_any = AnyType(TypeOfAny.special_form)
	mapping = cls_def_ctx.api.lookup_fully_qualified_or_none("typing.Mapping")
	mutable_mapping = cls_def_ctx.api.lookup_fully_qualified_or_none("typing.MutableMapping")
	mapping_str_any_type = Instance(mapping.node, [str_type, implicit_any])  # type: ignore
	mutable_mapping_str_any_type = Instance(mutable_mapping.node, [str_type, implicit_any])  # type: ignore
	# # maybe_mapping_str_any = UnionType.make_union([typ, NoneType()])(mapping_str_any_type)
	decorated_class_instance = Instance(
			cls_def_ctx.api.lookup_fully_qualified_or_none(cls_def_ctx.cls.fullname).node,  # type: ignore
			[],
			)

	if "to_dict" not in info.names:
		add_method_to_class(
				api=cls_def_ctx.api,
				cls=cls_def_ctx.cls,
				name="to_dict",
				args=[Argument(Var("convert_values", bool_type), bool_type, None, ARG_OPT)],
				return_type=mutable_mapping_str_any_type,
				)

	if "from_dict" not in info.names:
		add_classmethod_to_class(
				api=cls_def_ctx.api,
				cls=cls_def_ctx.cls,
				name="from_dict",
				args=[Argument(Var('d', mapping_str_any_type), mapping_str_any_type, None, ARG_POS)],
				return_type=decorated_class_instance,
				cls_type=TypeType(decorated_class_instance),
				)


#
# def attr__make_attrs(cls_def_ctx: ClassDefContext):
# 	"""
# 	Handles :func:attr.ib`.
#
# 	:param cls_def_ctx:
# 	"""
#
# 	info = cls_def_ctx.cls.info
#
# 	list_ = cls_def_ctx.api.lookup_fully_qualified_or_none('typing.List')
# 	attribute = cls_def_ctx.api.lookup_fully_qualified_or_none('attr.Attribute')
# 	#
# 	# if "__attrs_attrs__" not in info.names:
# 	# 	info.names["__attrs_attrs__"] = SymbolTableNode(
# 	# 			MDEF,
# 	# 			Var("__attrs_attrs__", Instance(list_.node, [attribute])),  # type: ignore
# 	# 			plugin_generated=True,
# 	# 			)

decorator_registry["attr_utils.serialise.serde"] = attr_utils_serialise_serde
# decorator_registry["attr._make.attrs"] = attr__make_attrs
# decorator_registry["attr.s"] = attr__make_attrs
# decorator_registry["attr.attrs"] = attr__make_attrs


class AttrUtilsPlugin(Plugin):
	"""
	Plugin for :github:repo:`mypy <python/mypy>` which adds support for ``attr_utils``.

	.. autoclasssumm:: AttrUtilsPlugin
		:autosummary-sections: ;;
	"""

	def get_class_decorator_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
		"""
		Allows mypy to handle decorators that add extra methods to classes.

		:param fullname: The full name of the decorator.
		"""

		return decorator_registry.get(fullname, None)


def add_classmethod_to_class(
		api: SemanticAnalyzerPluginInterface,
		cls: ClassDef,
		name: str,
		args: List[Argument],
		return_type: Type,
		cls_type: Optional[Type] = None,
		tvar_def: Optional[Any] = None,
		) -> None:
	"""
	Adds a new classmethod to a class definition.

	:param api:
	:param cls:
	:param name:
	:param args:
	:param return_type:
	:param cls_type:
	:param tvar_def:
	"""

	info = cls.info

	# First remove any previously generated methods with the same name
	# to avoid clashes and problems in the semantic analyzer.
	if name in info.names:
		sym = info.names[name]
		if sym.plugin_generated and isinstance(sym.node, FuncDef):
			cls.defs.body.remove(sym.node)

	cls_type = cls_type or fill_typevars(info)
	function_type = api.named_type(f"{_builtins}.function")

	args = [Argument(Var("cls"), cls_type, None, ARG_POS)] + args
	arg_types, arg_names, arg_kinds = [], [], []
	for arg in args:
		assert arg.type_annotation, "All arguments must be fully typed."
		arg_types.append(arg.type_annotation)
		arg_names.append(arg.variable.name)
		arg_kinds.append(arg.kind)

	signature = CallableType(arg_types, arg_kinds, arg_names, return_type, function_type)
	if tvar_def:
		signature.variables = [tvar_def]

	func = FuncDef(name, args, Block([PassStmt()]))
	func.is_class = True
	func.info = info
	func.type = set_callable_name(signature, func)
	func._fullname = info.fullname + '.' + name
	func.line = info.line

	# NOTE: we would like the plugin generated node to dominate, but we still
	# need to keep any existing definitions so they get semantically analyzed.
	if name in info.names:
		# Get a nice unique name instead.
		r_name = get_unique_redefinition_name(name, info.names)
		info.names[r_name] = info.names[name]

	info.names[name] = SymbolTableNode(MDEF, func, plugin_generated=True)
	info.defn.defs.body.append(func)


def plugin(version: str):
	"""
	Entry point to :mod:`attr_utils.mypy_plugin`.

	:param version: The current mypy version.
	"""

	# ignore version argument if the plugin works with all mypy versions.
	return AttrUtilsPlugin
