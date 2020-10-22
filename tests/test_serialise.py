# stdlib
from collections import Counter
from enum import IntEnum
from typing import Any, Mapping, MutableMapping, no_type_check

# 3rd party
import attr
import sdjson
from sdjson import register_encoder
from typing_extensions import Literal, Protocol, runtime_checkable

# this package
from attr_utils.serialise import serde


class DeviceType(IntEnum):
	RC = 1
	SCIC = 2


class Port(IntEnum):
	HDMI = 1
	VGA = 2
	DVI = 3
	DP = 4
	SCART = 5


@serde
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
	configuration: MutableMapping[str, Any] = attr.ib(default=attr.Factory(dict))


@attr.s(slots=True)
class EnhancedDevice(Device):
	"""
	A :class:`~.Device` with more features!
	"""

	warp_drive: Literal["Engaged!"] = attr.ib(default="Engaged!")


class MagicMapping(dict):
	pass


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

	assert d.to_dict() == {
			"device_id": 1000,
			"display_name": "Television",
			"device_type": DeviceType.RC,
			"configuration": {
					"make": "Samsung",
					"smart": True,
					"ports": Counter({Port.HDMI: 3, Port.VGA: 1}),
					},
			}

	device = Device.from_dict({
			"device_id": 1000,
			"display_name": "Television",
			"device_type": DeviceType.RC,
			"configuration": {
					"make": "Samsung",
					"smart": True,
					"ports": Counter({Port.HDMI: 3, Port.VGA: 1}),
					},
			})

	assert device == d
	assert isinstance(device, Device)


def test_collection_types():

	d = Device(
			1000,
			"Television",
			DeviceType.RC,
			MagicMapping(
					make="Samsung",
					smart=True,
					ports=Counter([Port.HDMI, Port.HDMI, Port.HDMI, Port.VGA]),
					),
			)

	assert isinstance(d.to_dict()["configuration"], MagicMapping)


def test_enhanced_device():
	e = EnhancedDevice(
			1000,
			"Television",
			DeviceType.RC,
			{
					"make": "Samsung",
					"smart": True,
					"ports": Counter([Port.HDMI, Port.HDMI, Port.HDMI, Port.VGA]),
					},
			)

	assert attr.asdict(e) == {
			"device_id": 1000,
			"display_name": "Television",
			"device_type": DeviceType.RC,
			"configuration": {
					"make": "Samsung",
					"smart": True,
					"ports": Counter({Port.HDMI: 3, Port.VGA: 1}),
					},
			"warp_drive": "Engaged!",
			}

	assert e.to_dict() == {
			"device_id": 1000,
			"display_name": "Television",
			"device_type": DeviceType.RC,
			"configuration": {
					"make": "Samsung",
					"smart": True,
					"ports": Counter({Port.HDMI: 3, Port.VGA: 1}),
					},
			"warp_drive": "Engaged!",
			}

	assert (
			EnhancedDevice.from_dict({
					"device_id": 1000,
					"display_name": "Television",
					"device_type": DeviceType.RC,
					"configuration": {
							"make": "Samsung",
							"smart": True,
							"ports": Counter({Port.HDMI: 3, Port.VGA: 1}),
							},
					"warp_drive": "Engaged!",
					}) == e
			)

	assert isinstance(
			EnhancedDevice.from_dict({
					"device_id": 1000,
					"display_name": "Television",
					"device_type": DeviceType.RC,
					"configuration": {
							"make": "Samsung",
							"smart": True,
							"ports": Counter({Port.HDMI: 3, Port.VGA: 1}),
							},
					"warp_drive": "Engaged!",
					}),
			EnhancedDevice,
			)


@no_type_check
def test_dunders():
	assert Device.to_dict.__module__ == "tests.test_serialise"
	assert Device.to_dict.__name__ == "to_dict"
	assert Device.to_dict.__qualname__ == "Device.to_dict"
	assert Device.to_dict.__annotations__ == {"convert_values": bool, "return": MutableMapping[str, Any]}

	assert Device.from_dict.__module__ == "tests.test_serialise"
	assert Device.from_dict.__name__ == "from_dict"
	assert Device.from_dict.__qualname__ == "Device.from_dict"
	assert Device.from_dict.__annotations__ == {"d": Mapping[str, Any]}

	assert EnhancedDevice.to_dict.__module__ == "tests.test_serialise"
	assert EnhancedDevice.to_dict.__name__ == "to_dict"
	assert EnhancedDevice.to_dict.__qualname__ == "Device.to_dict"
	assert EnhancedDevice.to_dict.__annotations__ == {"convert_values": bool, "return": MutableMapping[str, Any]}

	assert EnhancedDevice.from_dict.__module__ == "tests.test_serialise"
	assert EnhancedDevice.from_dict.__name__ == "from_dict"
	assert EnhancedDevice.from_dict.__qualname__ == "Device.from_dict"
	assert EnhancedDevice.from_dict.__annotations__ == {"d": Mapping[str, Any]}


@runtime_checkable
class HasToDict(Protocol):

	def to_dict(self):
		...


@register_encoder(HasToDict)
def serialise_attrs(obj: HasToDict):
	return obj.to_dict()


def test_sdjson():
	d = Device(
			1000,
			"Television",
			DeviceType.RC,
			MagicMapping(
					make="Samsung",
					smart=True,
					ports=Counter([Port.HDMI, Port.HDMI, Port.HDMI, Port.VGA]),
					),
			)

	expected = """{
  "device_id": 1000,
  "display_name": "Television",
  "device_type": 1,
  "configuration": {
    "make": "Samsung",
    "smart": true,
    "ports": {
      "1": 3,
      "2": 1
    }
  }
}"""

	assert sdjson.dumps(d, indent=2) == expected

	loaded_device = Device.from_dict(sdjson.loads(sdjson.dumps(d)))
	# the Counter won't be equal because the enum's have become disassociated
	assert loaded_device.device_id == d.device_id
	assert loaded_device.display_name == d.display_name
	assert loaded_device.configuration["make"] == d.configuration["make"]
	assert loaded_device.configuration["smart"] == d.configuration["smart"]
