.. py:currentmodule:: lsst.ts.dynalenegui

.. _lsst.ts.dynalenegui-version_history:

##################
Version History
##################

.. _lsst.ts.dynalenegui-0.2.0:

-------------
0.2.0
-------------

* Fix the package name in ``setup.py`` and add the ``pyproject.toml``.
* Add **ts_guitool** as a dependency.
* Add the tab classes based on **TabTemplate** and open them from the command list in **MainWindow**.
* Use the ``create_group_box()`` and ``create_label()`` of **ts_guitool** in **MainWindow**.
* Enable the **ruff** and **insert-license** pre-commit hooks.
* Add the unit tests of **MainWindow**.

-------------
0.1.0
-------------

* Initial framework.