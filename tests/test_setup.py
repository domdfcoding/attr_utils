# 3rd party
from sphinx_autodoc_typehints import builder_ready, process_signature

# this package
import attr_utils.autodoc_typehints


class MockApp:

	def __init__(self):
		self.config_values = []
		self.directives = []
		self.connections = []

	def add_config_value(self, *args, **kwargs):
		self.config_values.append(args)

	def add_directive(self, *args, **kwargs):
		self.directives.append(args)

	def connect(self, *args, **kwargs):
		self.connections.append(args)


def test_setup():
	app = MockApp()

	assert attr_utils.autodoc_typehints.setup(app=app) == {  # type: ignore
			"parallel_read_safe": True,
			}

	assert app.config_values == [
			('set_type_checking_flag', False, 'html'),
			('always_document_param_types', False, 'html'),
			('typehints_fully_qualified', False, 'env'),
			('typehints_document_rtype', True, 'env'),
			]
	assert app.connections == [
			('builder-inited', builder_ready),
			('autodoc-process-signature', process_signature),
			('autodoc-process-docstring', attr_utils.autodoc_typehints.process_docstring),
			]
