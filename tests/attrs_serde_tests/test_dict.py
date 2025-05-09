# stdlib
from typing import TYPE_CHECKING

# 3rd party
from attr import attrib, attrs

# this package
from attr_utils.serialise import serde

if TYPE_CHECKING:
	# 3rd party
	from snapshottest.pytest import PyTestSnapshotTest  # type: ignore[import]

person_dict = {"contact": {"personal": {"name": "John"}, "phone": "555-112233"}}
city_dict = {"name": "Tel-Aviv", "zipcode": "6100000"}

name_path = ["contact", "personal", "name"]
phone_path = ["contact", "phone"]


@serde
@attrs
class Person:
	name = attrib(metadata={"to": name_path, "from": name_path})
	phone = attrib(metadata={"to": phone_path, "from": phone_path})


@serde
@attrs
class Contact(Person):
	zip_code = attrib(default=56000, metadata={"to": phone_path})
	address = attrib(default="Abby Rd.")


@serde
@attrs
class City:
	name = attrib()
	zipcode = attrib()


@serde(from_key="get", to_key="set")
@attrs
class GetSet:
	name = attrib(metadata={"set": ["nameeee"], "get": ["name"]})

	phone = attrib(metadata={"set": ["phoneeee"], "get": ["phone"]})


def test_from_to_keys(snapshot: "PyTestSnapshotTest"):
	g = GetSet.from_dict({"name": "John", "phone": "555-1111"})
	snapshot.assert_match({"name": g.name, "phone": g.phone})
	snapshot.assert_match(g.to_dict())


def test_deser(snapshot: "PyTestSnapshotTest"):
	p = Person.from_dict(person_dict)
	snapshot.assert_match({"name": p.name, "phone": p.phone})


def test_ser(snapshot: "PyTestSnapshotTest"):
	snapshot.assert_match(Person(name="Slash", phone="555-334455").to_dict())


def test_ser_with_default_values(snapshot: "PyTestSnapshotTest"):
	p_dict = City(name="Tel-Aviv", zipcode="6100000").to_dict()
	snapshot.assert_match({"name": p_dict.get("name"), "zipcode": p_dict.get("zipcode")})


def test_quirky_object(snapshot: "PyTestSnapshotTest"):
	c = Contact.from_dict(person_dict)
	snapshot.assert_match({"name": c.name, "phone": c.phone, "zip": c.zip_code})


def test_irrelevant_object():
	c = Contact.from_dict({"irrelevant": True})


def test_deser_with_default_values(snapshot: "PyTestSnapshotTest"):
	p = City(name="Tel-Aviv", zipcode="6100000")
	snapshot.assert_match({"name": p.name, "zipcode": p.zipcode})
