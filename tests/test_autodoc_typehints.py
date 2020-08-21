#  Based on https://github.com/agronholm/sphinx-autodoc-typehints
#  Copyright (c) Alex Grönholm
#  MIT Licensed
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
import pathlib
import re
import sys
import textwrap
import typing
from typing import (
		Any, AnyStr, Callable, Dict, Generic, Mapping, NewType, Optional, Pattern, Tuple, Type, TypeVar, Union
		)

# 3rd party
import pytest
import typing_extensions

# this package
from attr_utils.autodoc_typehints import format_annotation, process_docstring

try:
	# stdlib
	from typing import IO
except ImportError:
	# stdlib
	from typing.io import IO

T = TypeVar('T')
U = TypeVar('U', covariant=True)
V = TypeVar('V', contravariant=True)
W = NewType('W', str)


class A:

	def get_type(self):
		return type(self)

	class Inner:
		pass


class B(Generic[T]):
	# This is set to make sure the correct class name ("B") is picked up
	name = 'Foo'


class C(B[str]):
	pass


class D(typing_extensions.Protocol):
	pass


class E(typing_extensions.Protocol[T]):
	pass


class Slotted:
	__slots__ = ()


class Metaclass(type):
	pass


@pytest.mark.parametrize(
		'annotation, expected_result',
		[(str, ':py:class:`str`'), (int, ':py:class:`int`'), (type(None), ':py:obj:`None`'),
			(type, ':py:class:`type`'), (Type, ':py:class:`~typing.Type`'),
			(Type[A], ':py:class:`~typing.Type`\\[:py:class:`~%s.A`]' % __name__), (Any, ':py:data:`~typing.Any`'),
			(AnyStr, ':py:data:`~typing.AnyStr`'), (Generic[T], ':py:class:`~typing.Generic`\\[\\:py:data:`~T`]'),
			(Mapping, ':py:class:`~typing.Mapping`'),
			(Mapping[T, int], ':py:class:`~typing.Mapping`\\[\\:py:data:`~T`, :py:class:`int`]'),
			(Mapping[str, V], ':py:class:`~typing.Mapping`\\[:py:class:`str`, \\:py:data:`-V`]'),
			(Mapping[T, U], ':py:class:`~typing.Mapping`\\[\\:py:data:`~T`, \\:py:data:`+U`]'),
			(Mapping[str, bool], ':py:class:`~typing.Mapping`\\[:py:class:`str`, '
				':py:class:`bool`]'), (Dict, ':py:class:`~typing.Dict`'),
			(Dict[T, int], ':py:class:`~typing.Dict`\\[\\:py:data:`~T`, :py:class:`int`]'),
			(Dict[str, V], ':py:class:`~typing.Dict`\\[:py:class:`str`, \\:py:data:`-V`]'),
			(Dict[T, U], ':py:class:`~typing.Dict`\\[\\:py:data:`~T`, \\:py:data:`+U`]'),
			(Dict[str, bool], ':py:class:`~typing.Dict`\\[:py:class:`str`, '
				':py:class:`bool`]'), (Tuple, ':py:data:`~typing.Tuple`'),
			(Tuple[str, bool], ':py:data:`~typing.Tuple`\\[:py:class:`str`, '
				':py:class:`bool`]'), (
						Tuple[int, int, int],
						':py:data:`~typing.Tuple`\\[:py:class:`int`, '
						':py:class:`int`, :py:class:`int`]'
						), (Tuple[str, ...], ':py:data:`~typing.Tuple`\\[:py:class:`str`, ...]'),
			(Union, ':py:data:`~typing.Union`'),
			(Union[str, bool], ':py:data:`~typing.Union`\\[:py:class:`str`, '
				':py:class:`bool`]'),
			pytest.param(
					Union[str, Any],
					':py:data:`~typing.Union`\\[:py:class:`str`, '
					':py:data:`~typing.Any`]',
					marks=pytest.mark.skipif((3, 5, 0) <= sys.version_info[:3] <= (3, 5, 2),
												reason='Union erases the str on 3.5.0 -> 3.5.2')
					), (Optional[str], ':py:data:`~typing.Optional`\\[:py:class:`str`]'),
			(Callable, ':py:data:`~typing.Callable`'),
			(Callable[..., int], ':py:data:`~typing.Callable`\\[..., :py:class:`int`]'),
			(Callable[[int], int], ':py:data:`~typing.Callable`\\[\\[:py:class:`int`], '
				':py:class:`int`]'),
			(
					Callable[[int, str], bool],
					':py:data:`~typing.Callable`\\[\\[:py:class:`int`, '
					':py:class:`str`], :py:class:`bool`]'
					),
			(
					Callable[[int, str], None],
					':py:data:`~typing.Callable`\\[\\[:py:class:`int`, '
					':py:class:`str`], :py:obj:`None`]'
					), (Callable[[T], T], ':py:data:`~typing.Callable`\\[\\[\\:py:data:`~T`], \\:py:data:`~T`]'),
			(Pattern, ':py:class:`~typing.Pattern`'),
			(Pattern[str], ':py:class:`~typing.Pattern`\\[:py:class:`str`]'), (IO, ':py:class:`~typing.IO`'),
			(IO[str], ':py:class:`~typing.IO`\\[:py:class:`str`]'),
			(Metaclass, ':py:class:`~%s.Metaclass`' % __name__), (A, ':py:class:`~%s.A`' % __name__),
			(B, ':py:class:`~%s.B`' % __name__), (B[int], ':py:class:`~%s.B`\\[:py:class:`int`]' % __name__),
			(C, ':py:class:`~%s.C`' % __name__), (D, ':py:class:`~%s.D`' % __name__),
			(E, ':py:class:`~%s.E`' % __name__), (E[int], ':py:class:`~%s.E`\\[:py:class:`int`]' % __name__),
			(W, ':py:func:`~typing.NewType`\\(:py:data:`~W`, :py:class:`str`)')]
		)
def test_format_annotation(inv, annotation, expected_result):
	result = format_annotation(annotation)
	assert result == expected_result

	# Test with the "fully_qualified" flag turned on
	if 'typing' in expected_result or __name__ in expected_result:
		expected_result = expected_result.replace('~typing', 'typing')
		expected_result = expected_result.replace('~' + __name__, __name__)
		assert format_annotation(annotation, fully_qualified=True) == expected_result

	# Test for the correct role (class vs data) using the official Sphinx inventory
	if 'typing' in expected_result:
		m = re.match('^:py:(?P<role>class|data|func):`~(?P<name>[^`]+)`', result)
		assert m, 'No match'
		name = m.group('name')
		expected_role = next((o.role for o in inv.objects if o.name == name), None)
		if expected_role:
			if expected_role == 'function':
				expected_role = 'func'

			assert m.group('role') == expected_role


@pytest.mark.parametrize('library', [typing, typing_extensions], ids=['typing', 'typing_extensions'])
@pytest.mark.parametrize(
		'annotation, params, expected_result',
		[('ClassVar', int, ":py:data:`~typing.ClassVar`\\[:py:class:`int`]"),
			('NoReturn', None, ":py:data:`~typing.NoReturn`"),
			('Literal', ('a', 1), ":py:data:`~typing.Literal`\\['a', 1]"),
			('Type', None, ':py:class:`~typing.Type`'),
			('Type', (A, ), ':py:class:`~typing.Type`\\[:py:class:`~%s.A`]' % __name__)]
		)
def test_format_annotation_both_libs(inv, library, annotation, params, expected_result):
	try:
		annotation_cls = getattr(library, annotation)
	except AttributeError:
		pytest.skip(f'{annotation} not available in the {library.__name__} module')

	ann = annotation_cls if params is None else annotation_cls[params]
	result = format_annotation(ann)
	assert result == expected_result


def test_process_docstring_slot_wrapper():
	lines = []
	process_docstring(None, 'class', 'SlotWrapper', Slotted, None, lines)
	assert not lines
