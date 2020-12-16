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
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/attr_utils/latest?logo=read-the-docs
	:target: https://attr_utils.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/attr_utils/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/attr_utils/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/attr_utils/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/attr_utils/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/attr_utils/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/attr_utils/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/attr_utils/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/attr_utils/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |requires| image:: https://requires.io/github/domdfcoding/attr_utils/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/attr_utils/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/attr_utils/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/attr_utils?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/attr_utils?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/attr_utils
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/attr_utils
	:target: https://pypi.org/project/attr_utils/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/attr_utils?logo=python&logoColor=white
	:target: https://pypi.org/project/attr_utils/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/attr_utils
	:target: https://pypi.org/project/attr_utils/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/attr_utils
	:target: https://pypi.org/project/attr_utils/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/attr_utils?logo=anaconda
	:target: https://anaconda.org/domdfcoding/attr_utils
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/attr_utils?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/attr_utils
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/attr_utils
	:target: https://github.com/domdfcoding/attr_utils/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/attr_utils
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/attr_utils/v0.5.5
	:target: https://github.com/domdfcoding/attr_utils/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/attr_utils
	:target: https://github.com/domdfcoding/attr_utils/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/attr_utils/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/attr_utils/master
	:alt: pre-commit.ci status

.. end shields

|

Installation
--------------

.. start installation

``attr_utils`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install attr_utils

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels http://conda.anaconda.org/domdfcoding
		$ conda config --add channels http://conda.anaconda.org/conda-forge

	* Then install

	.. code-block:: bash

		$ conda install attr_utils

.. end installation
