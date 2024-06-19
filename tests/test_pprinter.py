import __future__

# stdlib
import sys
from collections import Counter
from enum import IntEnum
from textwrap import dedent
from typing import Any, Dict, get_type_hints

# 3rd party
import attr
from coincidence import PEP_563

# this package
from attr_utils.pprinter import pretty_repr


class DeviceType(IntEnum):
	RC = 1
	SCIC = 2


class Port(IntEnum):
	HDMI = 1
	VGA = 2
	DVI = 3
	DP = 4
	SCART = 5


@pretty_repr
@attr.s(slots=True)
class Device:
	"""
	Represents a device in an :class:`~.AcqMethod`.
	"""

	#: The ID of the device
	device_id: int = attr.ib(converter=int)

	#: The display name for the device.
	display_name: str = attr.ib(converter=str)

	#: The type of device.
	device_type: DeviceType = attr.ib(converter=DeviceType)

	#: Key: value mapping of configuration options.
	configuration: Dict[str, Any] = attr.ib(default=attr.Factory(dict))


def test_device():

	d = Device(
			1000,
			"Television",
			DeviceType.RC,
			{
					"make": "Samsung",
					"smart": True,
					"ports": Counter([Port.HDMI, Port.HDMI, Port.HDMI, Port.VGA]),
					},
			)

	if sys.version_info >= (3, 14):
		expected = """tests.test_pprinter.Device(
	device_id=1000,
	display_name='Television',
	device_type=DeviceType.RC,
	configuration={
		'make': 'Samsung',
		'smart': True,
		'ports': collections.Counter({Port.HDMI: 3, Port.VGA: 1})
	}
)"""
	else:
		expected = """tests.test_pprinter.Device(
	device_id=1000,
	display_name='Television',
	device_type=<DeviceType.RC: 1>,
	configuration={
		'make': 'Samsung',
		'smart': True,
		'ports': collections.Counter({<Port.HDMI: 1>: 3, <Port.VGA: 2>: 1})
	}
)"""
	assert repr(d) == dedent(expected).expandtabs(4)


def test_dunders():
	assert Device.__repr__.__module__ == "tests.test_pprinter"
	assert Device.__repr__.__name__ == "__repr__"
	assert Device.__repr__.__qualname__ == "Device.__repr__"

	if PEP_563 and not hasattr(__future__, "co_annotations"):
		assert Device.__repr__.__annotations__ == {"return": "str"}
	else:
		assert Device.__repr__.__annotations__ == {"return": str}

	assert get_type_hints(Device.__repr__) == {"return": str}
