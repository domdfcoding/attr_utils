"""
This example is based on real code.
"""

# stdlib
from typing import Any, Dict, List, Sequence, Tuple

# 3rd party
import attr
from domdf_python_tools.utils import strtobool

# this package
from attr_utils.annotations import attrib


@attr.s(slots=True)
class Device:
	"""
	Represents a device in an :class:`~.AcqMethod`.

	:param device_id: The ID of the device
	:param display_name: The display name for the device.
	:param rc_device: Flag to indicate the device is an RC Device. If :py:obj:`False` the device is an SCIC.
	:param configuration: List of key: value mappings for configuration options.
	:param configuration2: Alternative form of ``configuration``.
	:param configuration3: Alternative form of ``configuration``.
	"""

	device_id: str = attr.ib(converter=str)
	display_name: str = attr.ib(converter=str)
	rc_device: bool = attr.ib(converter=strtobool)
	configuration: List[Dict[str, Any]] = attr.ib(converter=list, default=attr.Factory(list))
	configuration2: Tuple[Dict[str, Any]] = attr.ib(converter=tuple, default=attr.Factory(list))
	configuration3: List[Dict[str, Any]] = attr.ib(
			converter=list,
			default=attr.Factory(list),
			metadata={"annotation": Sequence[Dict[str, Any]]},
			)
	configuration4: List[Dict[str, Any]] = attrib(
			converter=list,
			default=attr.Factory(list),
			annotation=Sequence[Dict[str, Any]],
			)
