# stdlib
import sys

# 3rd party
import pytest
import sphinx
from bs4 import BeautifulSoup  # type: ignore[import]
from sphinx_toolbox.testing import HTMLRegressionFixture


def test_build(patched_app):
	patched_app.build()
	patched_app.build()


@pytest.mark.parametrize("page", ["annotations.html", "docstrings.html"], indirect=True)
def test_html_output(page: BeautifulSoup, html_regression: HTMLRegressionFixture):

	if sphinx.version_info >= (4, 3):  # pragma: no cover
		for div in page.select(
				"span.n span.pre,em.property span.pre,span.sig-name span.pre,span.sig-prename span.pre"
				):
			div.replace_with(div.text)

	for div in page.select("section"):
		children = tuple(div.children)
		if len(children) == 3 and children[1].name == "h2":
			# Move sibling into section
			siblings = list(div.parent.children)
			next_sibling = siblings[siblings.index(div) + 2]
			div.append(next_sibling.extract())

	html_regression.check(page, jinja2=True)


@pytest.mark.parametrize("page", ["autoattrs.html"], indirect=True)
def test_html_output_autoattrs(page: BeautifulSoup, html_regression: HTMLRegressionFixture):

	if sphinx.version_info >= (4, 3):  # pragma: no cover
		for div in page.select(
				"span.n span.pre,span.o span.pre,span.p span.pre,em.property span.pre,em.property span.p,span.sig-name span.pre,span.sig-prename span.pre,span.default_value span.pre,span.sig-return"
				):
			div.replace_with(div.text)

	for div in page.select("dl.attribute em.property"):
		new_tag = page.new_tag("em", attrs={"class": "property"})
		new_tag.string = div.text
		div.replace_with(new_tag)

	html_regression.check(page, jinja2=True)



