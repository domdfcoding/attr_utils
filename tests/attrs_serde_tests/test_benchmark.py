# 3rd party
import pytest
from attr import asdict, attrib, attrs

# this package
from attr_utils.serialise import serde

name_path = ["contact", "personal", "name"]
phone_path = ["contact", "phone"]


@serde
@attrs
class Person:
	name = attrib(metadata={"to": name_path, "from": name_path})
	phone = attrib(metadata={"to": phone_path, "from": phone_path})


person_dict = {"contact": {"personal": {"name": "John"}, "phone": "555-112233"}}
person = Person(name="James", phone="555-666222")


@pytest.mark.benchmark(group="serialization")
def test_ser_baseline(benchmark):

	def baseline():
		asdict(person)

	benchmark(baseline)


@pytest.mark.benchmark(group="serialization")
def test_ser_serde(benchmark):

	def serde():
		person.to_dict()

	benchmark(serde)


@pytest.mark.benchmark(group="deserialization")
def test_deser_baseline(benchmark):

	def baseline():
		Person(
				name=person_dict["contact"]["personal"]["name"],  # type: ignore
				phone=person_dict["contact"]["phone"],
				)

	benchmark(baseline)


@pytest.mark.benchmark(group="deserialization")
def test_deser_serde(benchmark):

	def serde():
		p = Person.from_dict(person_dict)

	benchmark(serde)
