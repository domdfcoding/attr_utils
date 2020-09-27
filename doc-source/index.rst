###########
attr_utils
###########

.. start short_desc

**Utilities to augment attrs.**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| rtfd-shield::
	:project: attr_utils
	:alt: Documentation Build Status

.. |docs_check| actions-shield::
	:workflow: Docs Check
	:alt: Docs Check Status

.. |travis| travis-shield::
	:travis-site: com
	:alt: Travis Build Status

.. |actions_windows| actions-shield::
	:workflow: Windows Tests
	:alt: Windows Tests Status

.. |actions_macos| actions-shield::
	:workflow: macOS Tests
	:alt: macOS Tests Status

.. |requires| requires-io-shield::
	:alt: Requirements Status

.. |coveralls| coveralls-shield::
	:alt: Coverage

.. |codefactor| codefactor-shield::
	:alt: CodeFactor Grade

.. |pypi-version| pypi-shield::
	:project: attr_utils
	:version:
	:alt: PyPI - Package Version

.. |supported-versions| pypi-shield::
	:project: attr_utils
	:py-versions:
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| pypi-shield::
	:project: attr_utils
	:implementations:
	:alt: PyPI - Supported Implementations

.. |wheel| pypi-shield::
	:project: attr_utils
	:wheel:
	:alt: PyPI - Wheel

.. |license| github-shield::
	:license:
	:alt: License

.. |language| github-shield::
	:top-language:
	:alt: GitHub top language

.. |commits-since| github-shield::
	:commits-since: v0.3.1
	:alt: GitHub commits since tagged version

.. |commits-latest| github-shield::
	:last-commit:
	:alt: GitHub last commit

.. |maintained| maintained-shield:: 2020
	:alt: Maintenance

.. |pre_commit| pre-commit-shield::
	:alt: pre-commit

.. end shields

Installation
---------------

.. start installation

.. installation:: attr_utils
	:pypi:
	:github:

.. end installation


| ``attr_utils`` provides both utility functions and two Sphinx extensions: :mod:`attr_utils.annotations` and :mod:`attr_utils.autoattrs`.
| Enable the extensions by adding the following to the ``extensions`` variable in your ``conf.py``:

.. extensions:: attr_utils.autoattrs
	:no-preamble:

	sphinx.ext.autodoc
	sphinx_toolbox.more_autodoc.typehints
	attr_utils.annotations


.. toctree::
	:hidden:

	Home<self>
	demo

.. toctree::
	:maxdepth: 3
	:caption: API Reference
	:glob:

	api/*

.. toctree::
	:maxdepth: 3
	:caption: Contributing

	contributing
	Source

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/attr_utils>`__

.. end links
