# stdlib
from typing import Any, Callable, Dict, List, Tuple, get_type_hints

# 3rd party
import attr

# this package
from attr_utils.annotations import add_init_annotations


def my_converter(arg: List[Dict[str, Any]]):
	return arg


def untyped_converter(arg):
	return arg


@attr.s
class SomeClass:
	a_string: str = attr.ib(converter=str)
	custom_converter: Any = attr.ib(converter=my_converter)
	untyped: Tuple[str, int, float] = attr.ib(converter=untyped_converter)  # type: ignore
	no_converter: Callable[[str], None] = attr.ib()


def test_add_init_annotations():

	add_init_annotations(SomeClass)

	# print(SomeClass.__init__.__annotations__)
	assert SomeClass.__init__.__annotations__ == {
			'return': None,
			'a_string': str,
			'custom_converter': List[Dict[str, Any]],
			'untyped': Tuple[str, int, float],
			'no_converter': Callable[[str], None],
			}

	# print(typing.get_type_hints(SomeClass.__init__))
	assert get_type_hints(SomeClass.__init__) == {
			'return': type(None),
			'a_string': str,
			'custom_converter': List[Dict[str, Any]],
			'untyped': Tuple[str, int, float],
			'no_converter': Callable[[str], None],
			}


def test_add_init_annotations_not_attrs_class():

	assert not hasattr(str, "__attrs_attrs__")
	add_init_annotations(str)
