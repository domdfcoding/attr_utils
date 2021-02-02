# stdlib
import sys

# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture  # type: ignore
from sphinx_toolbox.testing import check_html_regression


def test_build(patched_app):
	patched_app.build()
	patched_app.build()


@pytest.mark.parametrize("page", ["annotations.html", "docstrings.html"], indirect=True)
def test_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	check_html_regression(page, file_regression)


@pytest.mark.skipif(condition=sys.version_info < (3, 7), reason="Output differs in Python 3.6")
@pytest.mark.parametrize("page", ["autoattrs.html"], indirect=True)
def test_html_output_autoattrs(page: BeautifulSoup, file_regression: FileRegressionFixture):
	check_html_regression(page, file_regression)


@pytest.mark.skipif(condition=sys.version_info[:2] > (3, 6), reason="Output differs in Python 3.6")
@pytest.mark.parametrize("page", ["autoattrs.html"], indirect=True)
def test_html_output_autoattrs_36(page: BeautifulSoup, file_regression: FileRegressionFixture):
	check_html_regression(page, file_regression)
