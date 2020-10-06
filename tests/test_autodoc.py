# this package
from attr_utils.annotations import AttrsClass
from attr_utils.autoattrs import AttrsDocumenter


def test_can_document():
	assert AttrsDocumenter.can_document_member(AttrsClass, "AttrsClass", False, None)
	assert not AttrsDocumenter.can_document_member(
			AttrsClass("Joe", 20, ["Plumber", "Apprentice"]),
			"joe",
			False,
			None,
			)
