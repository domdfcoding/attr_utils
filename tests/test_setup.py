# 3rd party
from sphinx_toolbox.testing import run_setup

# this package
from attr_utils import __version__, annotations


def test_setup():
	setup_ret, directives, roles, additional_nodes, app = run_setup(annotations.setup)

	assert setup_ret == {
			"version": __version__,
			"parallel_read_safe": True,
			}
	assert directives == {}
	assert roles == {}
	assert additional_nodes == set()
