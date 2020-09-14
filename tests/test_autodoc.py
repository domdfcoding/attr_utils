
from attr_utils.annotations import AttrsClass
from attr_utils.autoattrs import AttrsDocumenter


def test_can_document():
	assert AttrsDocumenter.can_document_member(AttrsClass, None, None, None)
