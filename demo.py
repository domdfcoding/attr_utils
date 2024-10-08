"""
This example is based on real code.
"""

# stdlib
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, overload

# 3rd party
import attrs
from domdf_python_tools.utils import strtobool

# this package
from attr_utils.annotations import attrib
from attr_utils.pprinter import pretty_repr
from attr_utils.serialise import serde


@pretty_repr
@serde
@attrs.define(slots=True, order=True)
class Device:
	"""
	Represents a device in an :class:`~.AcqMethod`.
	"""

	#: The ID of the device
	device_id: str = attrs.field(converter=str)

	#: The display name for the device.
	display_name: str = attrs.field(converter=str)

	rc_device: bool = attrs.field(converter=strtobool)
	"""
	Flag to indicate the device is an RC Device.
	If :py:obj:`False` the device is an SCIC.
	"""

	#: List of key: value mappings for configuration options.
	configuration: List[Dict[str, Any]] = attrs.field(converter=list, factory=list)

	#: Alternative form of ``configuration``.
	configuration2: Tuple[Dict[str, Any]] = attrs.field(
			converter=tuple,
			default=attrs.Factory(tuple),
			)

	#: Alternative form of ``configuration``.
	configuration3: List[Dict[str, Any]] = attrs.field(
			converter=list,
			default=attrs.Factory(list),
			metadata={"annotation": Sequence[Dict[str, Any]]},
			)

	#: Alternative form of ``configuration``.
	configuration4: List[Dict[str, Any]] = attrib(
			converter=list,
			factory=list,
			annotation=Sequence[Dict[str, Any]],
			)

	@overload
	def __getitem__(self, item: int) -> str: ...

	@overload
	def __getitem__(self, item: slice) -> List[str]: ...

	def __getitem__(self, item: Union[int, slice]) -> Union[str, List[str]]:
		"""
		Return the item with the given index.

		:param item:

		:rtype:

		.. versionadded:: 1.2.3
		"""


@attrs.define(init=False, order=True)
class Connector:
	"""
	Represents an electrical connector.

	:param name: The name of the connector.
	:param n_pins: The number if pins. For common connectors this is inferred from the name.
	:param right_angle: Whether this is a right angle connector.
	"""

	#: The name of the connector
	name: str = attrs.field(converter=str)

	#: The number of pins
	n_pins: int = attrs.field(converter=int)

	def __init__(self, name: str, n_pins: Optional[int] = None, right_angle: bool = False):
		if name == "DA-15":
			n_pins = 15
		elif name == "DB-25":
			n_pins = 25
		elif name == "DE-15":
			n_pins = 15

		self.__attrs_init__(name, n_pins)
