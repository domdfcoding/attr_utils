###########
attr_utils
###########

.. start short_desc

.. documentation-summary::
	:meta:

.. end short_desc

.. start shields

.. only:: html

	.. list-table::
		:stub-columns: 1
		:widths: 10 90

		* - Docs
		  - |docs| |docs_check|
		* - Tests
		  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
		* - PyPI
		  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
		* - Anaconda
		  - |conda-version| |conda-platform|
		* - Activity
		  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
		* - QA
		  - |codefactor| |actions_flake8| |actions_mypy|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: attr-utils
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/attr_utils/badge.svg
		:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/attr_utils/
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

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/attr_utils?logo=anaconda
		:target: https://anaconda.org/domdfcoding/attr_utils
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/attr_utils?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/attr_utils
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v1.1.0
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2024
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: attr_utils
		:downloads: month
		:alt: PyPI - Downloads

.. end shields

Installation
---------------

.. start installation

.. installation:: attr_utils
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation

.. attention::

	In v0.6.0 and above the :mod:`~.pprinter` module requires the ``pprint`` extra to be installed:

	.. prompt::

		python -m pip install attr-utils[pprint]

Overview
-----------------

``attr_utils`` provides both utility functions and two Sphinx extensions: :mod:`attr_utils.annotations` and :mod:`attr_utils.autoattrs`.

Enable the extensions by adding the following to the ``extensions`` variable in your ``conf.py``:

.. extensions:: attr_utils.autoattrs
	:no-preamble:

	sphinx.ext.autodoc
	sphinx_toolbox.more_autodoc.typehints
	attr_utils.annotations


Contents
---------------

.. html-section::

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:glob:

	demo
	api/*
	contributing
	Source
	license

.. sidebar-links::
	:caption: Links
	:github:
	:pypi: attr_utils


.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <domdfcoding/attr_utils>`

.. end links
