Methodology
===========
- Protect your main (DTAP) branches from direct commits. Commits shall only
  arrive into these branches via pull request.
- Use feature branches. Make your own prefixes (or use current ones) for
  classification of the ticket. Add ticket name to the name of the branch,
  followed by slugified ticket title.
- Prefix commits with ticket number followed by meaningful description.

Sample branch names:

- ``bugfix/MSFT-1240-LinkedIn-authentication-failing``
- ``deprecation/MSFT-1239-Deprecate-Python2``
- ``feature/MSFT-1238-Token-authentication``

Sample commit messages:

- ``MSFT-1240 Fix package configuration.``
- ``MSFT-1239 Deprecate Python2.``
- ``MSFT-1238 Implement token authentication.``
