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
Basic usage
-----------
See `Basic concepts <https://matyan.readthedocs.io/en/latest/basic_concepts.html>`_
section to get impression on possible commit methodology and assumptions taken.

**Generate changelog:**

.. code-block:: sh

    generate-changelog

**Generate changelog skipping orphaned commits:**

In some cases you would only want to show what has been done with tickets and
skip all non-ticket related commits.

.. code-block:: sh

    generate-changelog --no-other

**Generate changelog between two releases:**

In other cases you would want to show what has been done since last release.
The following example would generate changelog since version 0.0.1 to
version 0.0.3.

.. code-block:: sh

    generate-changelog 0.0.1..0.0.3

**Generate changelog between two branches:**

Sometimes you just need to show the changes made on acceptance since last
production release.
The following example would generate changelog with changes that are on
acceptance branch and not yet in master.

.. code-block:: sh

    generate-changelog master..acceptance

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

**Generate changelog with headings only (no commit messages) and releases info shown**

.. code-block:: sh

    generate-changelog --headings-only --show-releases

**Generate changelog between two branches, show unreleased changes only:**

.. code-block:: sh

    generate-changelog master..acceptance --show-releases --unreleased-only

Rendering
---------
The following renderers are implemented:

- Markdown
- RestructuredText
- Historical Markdown (for compatibility with ``matyan`` versions prior to
  0.4).

Markdown
~~~~~~~~
.. code-block:: sh

    generate-changelog --show-releases --renderer=markdown

RestructuredText
~~~~~~~~~~~~~~~~
.. code-block:: sh

    generate-changelog --show-releases --renderer=rest

Historical Markdown
~~~~~~~~~~~~~~~~~~~
.. code-block:: sh

    generate-changelog --show-releases --renderer=historical-markdown

Jira integration
----------------
It's possible to fetch ticket title and description from Jira. In order for it
to work, you should provide a ``fetch-title`` and ``fetch-description``
arguments:

.. code-block:: sh

    generate-changelog --show-releases --fetch-title --fetch-description

In adddition to that, you should put valid Jira credentials into your
global ``.matyan.ini`` configuration file.

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


Note, that placing ``.matyan.ini`` into the home root will make that
configuration global for all projects. That's however is handy, since local
``.matyan.ini`` files simply override the global ones. You could use global
configuration for instance for storing credentials to Jira.

.. code-block:: text

    [Jira]
    url:https://barseghyanartur.atlassian.net/
    username:user@domain.com
    token:abcd1234

Tips and tricks
===============
Write to file
-------------
.. code-block:: sh

    generate-changelog --show-releases 2>&1 | tee changelog.md

Create initial config file
--------------------------

.. code-block:: sh

    matyan-make-config

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
