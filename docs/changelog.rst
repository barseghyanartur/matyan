Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: none

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.4.3
-----
2019-12-26

- Ensure correct order of releases.
- Exclude unnecessary data from distribution.
- Add Jupyter notebook examples.
- Introduce debug mode (turned off by default). At the moment, logging is
  used in debug mode only.

0.4.2
-----
2019-12-25

- Minor speed-ups.
- Fix minor rendering issue with occasionally lost comments.
- Add logging.

0.4.1
-----
2019-12-24

- Prevent errors and infinite wait time on faulty connections (when fetching
  data from Jira).
- Minor speed ups.

0.4
---
2019-12-22

- Placing ``.matyan.ini`` config file (placed in the home root directory
  now makes it a global configuration). File placed locally may override the
  settings. That could be handy, among others, to store credentials to Jira,
  which you probably do not want to have versioned.
- Make it possible to fetch additional information (for now from Jira only,
  but can be extended).
- Softened the regular expression patterns for ticket numbers/branch names.
- Implemented renderer classes (at the moment markdown and restructured text).
- Updated default rendering of markdown (for better markup). If you need old
  style behaviour, use ``historical-markdown`` renderer.

0.3.4
-----
2019-11-27

- Add an option to show unreleased changes only.

0.3.3
-----
2019-11-24

- Minor fixes.
- More tests.

0.3.2
-----
2019-11-23

- Fixes in rendering logic.
- Added simple text beatification (capitalize, add final dot).

0.3.1
-----
2019-11-21

- Add ``headings-only`` option to generate headings only (no commit messages).
- Add date to feature branch data (JSON only yet).

0.3
---
2019-11-20

- Most of the functions got optional ``path`` parameter to use as
  path to the repository directory.
- ``matyan-create-config`` command renamed to ``matyan-make-config``.
- Next to the commands, functions are tested as well.
- Fix issue with lower edge nog being included when using dotted range.
- Added more tests.

0.2.1
-----
2019-11-19

- Minor fixes.

0.2
---
2019-11-19

- Hide empty sections/records.
- Add an option to generate changelog for latest release only.
- Handle multiple merge format commit messages.
- Prevent JSON decoding errors.
- Exclude tests from coverage.

0.1
---
2019-11-18

.. note::

    Release dedicated to my mother, who turned 70 yesterday.

- Status changed to beta.
- Minor fixes.
- Add `matyan-create-config` command.
- Add initial tests.

0.0.2
-----
2019-11-17

- Minor fixes.

0.0.1
-----
2019-11-17

- Initial alpha release.
