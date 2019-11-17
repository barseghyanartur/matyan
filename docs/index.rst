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
   :alt: MPL-1.1 OR GPL-2.0-only OR LGPL-2.1-or-later

.. image:: https://coveralls.io/repos/github/barseghyanartur/matyan/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/barseghyanartur/matyan?branch=master
    :alt: Coverage

Prerequisites
=============
- Python 3.6, 3.7, 3.8 and PyPy

Use cases and basic concepts
============================
If the following applies to you, ``matyan`` could help:

- Project releases (tags) are numbered according to the
  `semantic versioning <https://semver.org/>`_ or
  `sequence based identifiers <http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_.
- Project follows the DTAP.
- Testing, acceptance and production branches (hereafter referred as TAP
  branches) are protected.
- Direct commits to TAP branches are forbidden.
- All commits to TAP branches are made by pull requests.
- JIRA (or a similar tool) is used for handing project tickets.
- Pull requests are merged using GitHub or BitBucket web interface.

Sample use-case
---------------
The use-case
~~~~~~~~~~~~
- JIRA is used for issues.
- All commits are prefixed with ID of the JIRA issue: for example, `MSFT-1234`
  or `NVDA-1234` (where first four letters identify the client commit was done
  for, it's pattern).
- There are 3 main (protected) branches: `dev`, `staging`, `master`.
  Direct commits to any of the 3 are forbidden. Any feature/bugfix comes via
  merge request.
- All branches do have meaningful prefixes. Example,
  `feature/MSFT-1234-Title-of-the-issue` or
  `bugfix/MSFT-1236-prevent-duplicate-postal-codes`.
- Release flow is `dev` -> `staging` -> `master`.

Sample commits
~~~~~~~~~~~~~~
Consider the following commits into the dev branch:

*branch: bugfix/MSFT-1240-LinkedIn-authentication-failing*

- MSFT-1240 Fix package configuration.
- MSFT-1240 Update authentication pipeline.

*branch: deprecation/MSFT-1239-Deprecate-Python2*

- MSFT-1239 Deprecate Python2.
- MSFT-1238 Add initial MyPY setup.

*branch: feature/MSFT-1238-Token-authentication*

- MSFT-1238 Implement token authentication.
- MSFT-1238 Update authentication docs.

*branch: feature/MSFT-1237-Improve-document-sharing*

- MSFT-1237 Improve document sharing. Add option to share via GDrive.

*branch: bugfix/MSFT-1236-prevent-duplicate-postal-codes*

- MSFT-1236 Normalise postal codes for German addresses.
- MSFT-1236 Normalise postal codes for US addresses.
- MSFT-1236 Make postal code field unique for the country.

*branch: deprecation/MSFT-1235-deprecate-old-api*

- MSFT-1235 Deprecate API v 2.0.
- MSFT-1235 Update docs.

*branch: feature/MSFT-1234-car-type-suggester*

- MSFT-1234 Initial car type suggester implementation.
- MSFT-1234 Add insurance amount indication based on car weight.

Sample releases
~~~~~~~~~~~~~~~
All commits have been finally merged into master.

Releases have been made in the following way:

*0.1*

- Merged issues MSFT-1234, MSFT-1235 and MSFT-1236

*0.2*

- Merged issues MSFT-1237 and MSFT-1238

*Yet unreleased features/branches*

- MSFT-1239 and

Sample changelog output
-----------------------
The generated change log would look as follows:

.. code-block:: text

    ### 0.2

    **Features**

    *MSFT-1238 Token-authentication*

    - Implement token authentication.
    - Update authentication docs.

    *MSFT-1237 Improve document sharing*

    - Improve document sharing. Add option to share via GDrive.

    ### 0.1

    **Bugfixes**

    *MSFT-1236 Prevent duplicate postal codes*

    - Normalise postal codes for German addresses.
    - Normalise postal codes for US addresses.
    - Make postal code field unique for the country.

    **Deprecations**

    *MSFT-1235 Deprecate old api*

    - Deprecate API v 2.0.
    - Update docs.

    **Features**

    *MSFT-1234 Car type suggester*

    - Initial car type suggester implementation.
    - Add insurance amount indication based on car weight.

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

**Generate changelog with releases info shown**

.. code-block:: sh

    generate-changelog --show-releases

**Generate changelog between releases with releases info shown**

.. code-block:: sh

    generate-changelog 0.0.1..0.0.3 --show-releases

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
   changelog
   matyan

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
