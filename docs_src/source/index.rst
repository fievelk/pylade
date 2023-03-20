.. PyLaDe documentation master file, created by
   sphinx-quickstart on Mon Mar 20 12:17:52 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyLaDe's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

**PyLaDe** is a lightweight language detection tool written in Python. The tool provides a ready-to-use command-line interface, along with a more complex scaffolding for customized tasks.

The current version of PyLaDe implements the *Cavnar-Trenkle N-Gram-based approach*. However, the tool can be further expanded with customized language identification implementations.

If you just want to detect the language of a text, here is what you came for::

   $ pip install pylade
   $ pylade "What's the language of this sentence?"
   INFO : Identifying language...
   en

PyLaDe allows:
- training your own model
- using a custom language detection implementation

If you want more information about installing and using PyLaDe, you can find up-to-date instructions on the `project's repository <https://github.com/fievelk/pylade>`_.

If you are looking for technical information about models, classes and methods, please refer to the table of contents below.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
