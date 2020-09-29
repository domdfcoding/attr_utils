"""
This example is based on real code.
"""

# stdlib
from typing import Any, Dict, List, Sequence, Tuple, Union, overload

# 3rd party
import attr
from domdf_python_tools.utils import strtobool

# this package
from attr_utils.annotations import attrib
from attr_utils.pprinter import pretty_repr
from attr_utils.serialise import serde


@pretty_repr
@serde
@attr.s(slots=True)
class Device:
	"""
	Represents a device in an :class:`~.AcqMethod`.
	"""

	#: The ID of the device
	device_id: str = attr.ib(converter=str)

	#: The display name for the device.
	display_name: str = attr.ib(converter=str)

	#: Flag to indicate the device is an RC Device. If :py:obj:`False` the device is an SCIC.
	rc_device: bool = attr.ib(converter=strtobool)

	#: List of key: value mappings for configuration options.
	configuration: List[Dict[str, Any]] = attr.ib(converter=list, default=attr.Factory(list))

	#: Alternative form of ``configuration``.
	configuration2: Tuple[Dict[str, Any]] = attr.ib(converter=tuple, default=attr.Factory(list))

	#: Alternative form of ``configuration``.
	configuration3: List[Dict[str, Any]] = attr.ib(
			converter=list,
			default=attr.Factory(list),
			metadata={"annotation": Sequence[Dict[str, Any]]},
			)

	#: Alternative form of ``configuration``.
	configuration4: List[Dict[str, Any]] = attrib(
			converter=list,
			default=attr.Factory(list),
			annotation=Sequence[Dict[str, Any]],
			)

	@overload
	def __getitem__(self, item: int) -> str:
		...

	@overload
	def __getitem__(self, item: slice) -> List[str]:
		...

	def __getitem__(self, item: Union[int, slice]) -> Union[str, List[str]]:
		"""
		Return the item with the given index.

		:param item:

		:rtype:

		.. versionadded:: 1.2.3
		"""
