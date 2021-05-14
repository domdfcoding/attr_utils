# stdlib
import sys

# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from coincidence.regressions import AdvancedFileRegressionFixture
from sphinx_toolbox.testing import check_html_regression


def test_build(patched_app):
	patched_app.build()
	patched_app.build()


@pytest.mark.parametrize("page", ["annotations.html", "docstrings.html"], indirect=True)
def test_html_output(page: BeautifulSoup, advanced_file_regression: AdvancedFileRegressionFixture):
	check_html_regression(page, advanced_file_regression)


@pytest.mark.skipif(condition=sys.version_info < (3, 7), reason="Output differs in Python 3.6")
@pytest.mark.parametrize("page", ["autoattrs.html"], indirect=True)
def test_html_output_autoattrs(page: BeautifulSoup, advanced_file_regression: AdvancedFileRegressionFixture):
	check_html_regression(page, advanced_file_regression)


@pytest.mark.skipif(condition=sys.version_info[:2] > (3, 6), reason="Output differs in Python 3.6")
@pytest.mark.parametrize("page", ["autoattrs.html"], indirect=True)
def test_html_output_autoattrs_36(page: BeautifulSoup, advanced_file_regression: AdvancedFileRegressionFixture):
	check_html_regression(page, advanced_file_regression)
