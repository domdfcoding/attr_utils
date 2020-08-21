=================================
:mod:`attr_utils.autodoc_typehints`
=================================

Modified version of the `sphinx-autodoc-typehints <https://github.com/agronholm/sphinx-autodoc-typehints>`_ Sphinx extension which automatically adds type hints to the ``__init__`` method of `attrs <https://www.attrs.org>`_ classes.


Enable the extension by adding "attr_utils.autodoc_typehints" to the ``extensions`` variable in ``conf.py``:

.. code-block:: python

	extensions = [
		...
		"attr_utils.autodoc_typehints",
		]

For more information see https://www.sphinx-doc.org/en/master/usage/extensions/index.html#third-party-extensions .

If you are already using `sphinx-autodoc-typehints <https://github.com/agronholm/sphinx-autodoc-typehints>`__ remove its entry from the ``extensions`` list.
