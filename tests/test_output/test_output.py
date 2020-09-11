# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture  # type: ignore
from sphinx_toolbox.testing import check_html_regression


def test_build(app):
	app.build()
	app.build()


@pytest.mark.parametrize("page", ["index.html"], indirect=True)
def test_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	check_html_regression(page, file_regression)
