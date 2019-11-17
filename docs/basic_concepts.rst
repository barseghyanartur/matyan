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
