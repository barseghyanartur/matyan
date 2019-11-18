======
Matyan
======
Generate changelog from Git commits.

.. image:: https://img.shields.io/pypi/v/matyan.svg
   :target: https://pypi.python.org/pypi/matyan
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/matyan.svg
    :target: https://pypi.python.org/pypi/matyan/
    :alt: Supported Python versions

.. image:: https://img.shields.io/travis/barseghyanartur/matyan/master.svg
   :target: http://travis-ci.org/barseghyanartur/matyan
   :alt: Build Status

.. image:: https://img.shields.io/badge/license-GPL--2.0--only%20OR%20LGPL--2.1--or--later-blue.svg
   :target: https://github.com/barseghyanartur/matyan/#License
   :alt: GPL-2.0-only OR LGPL-2.1-or-later

.. image:: https://coveralls.io/repos/github/barseghyanartur/matyan/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/barseghyanartur/matyan?branch=master
    :alt: Coverage

Prerequisites
=============
- Python 3.6, 3.7 and 3.8

Documentation
=============
Documentation is available on `Read the Docs
<http://matyan.readthedocs.io/>`_.

Installation
============
Latest stable version on PyPI:

.. code-block:: sh

    pip install matyan

Usage
=====
See `Basic concepts <https://matyan.readthedocs.io/en/latest/basic_concepts.html>`_
section to get impression on possible commit methodology and assumptions taken.

**Generate changelog:**

.. code-block:: sh

    generate-changelog

**Generate changelog skipping orphaned commits:**

In some cases you only want to show what has been done with tickets and skip
all non-ticket related commits.

.. code-block:: sh

    generate-changelog --no-other

**Generate changelog between two releases:**

In some cases you only want to show what has been done since last release.
The following example would generate changelog since version 0.0.1 to
version 0.0.3.

.. code-block:: sh

    generate-changelog 0.0.1..0.0.3

**Generate changelog between two branches:**

In some cases you only want to show what has been done since last release.
The following example would generate changelog since version 0.0.1 to
version 0.0.3.

.. code-block:: sh

    generate-changelog master..dev

**Generate changelog with releases info shown**

.. code-block:: sh

    generate-changelog --show-releases

**Generate changelog between releases with releases info shown**

.. code-block:: sh

    generate-changelog 0.0.1..0.0.3 --show-releases

**Generate changelog between branches with releases info shown**

.. code-block:: sh

    generate-changelog master..dev --show-releases

**Generate changelog for the latest release with releases info shown**

.. code-block:: sh

    generate-changelog --latest-release --show-releases

Configuration
=============
In order to customize names and texts, add a ``.matyan.ini`` in your
project directory, form which you will be running the ``generate-changelog``
command.

Sample configuration:

.. code-block:: text

    [BranchTypes]
    feature: Feature
    bugfix: Bugfix
    hotfix: Hotfix
    deprecation: Deprecation

    [OtherBranchType]
    other: Other

    [Unreleased]
    unreleased: Unreleased

    [IgnoreCommits]
    exact: more
           clean up
           code comments
           more on docs
           repo
           working
           more on
           wip
           commit
    prefix: more on
            continue on


Tips and tricks
===============
Write to file
-------------
.. code-block:: sh

    generate-changelog --show-releases 2>&1 | tee changelog.md

Create initial config file
--------------------------

.. code-block:: sh

    matyan-create-config

Testing
=======
Simply type:

.. code-block:: sh

    ./runtests.py

Or use tox:

.. code-block:: sh

    tox

Or use tox to check specific env:

.. code-block:: sh

    tox -e py36

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======
GPL-2.0-only OR LGPL-2.1-or-later

Support
=======
For any issues contact me at the e-mail given in the `Author`_ section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>

Docs
====

Contents:

.. toctree::
   :maxdepth: 20

   index
   basic_concepts
   methodology
   changelog
   matyan

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
