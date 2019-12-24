#!/usr/bin/env bash
python -m cProfile \
  -o profile.cprof runtests.py src/matyan/tests/test_core.py::TestCore \
  -k "test_generate_changelog_show_releases and not rst and not historical and not headings and not unreleased"
pyprof2calltree -k -i profile.cprof
