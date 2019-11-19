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
