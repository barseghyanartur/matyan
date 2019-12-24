#!/usr/bin/env bash
pycallgraph graphviz \
  -- runtests.py src/matyan/tests/test_core.py::TestCore \
  -k "test_generate_changelog_show_releases and not rst and not historical and not headings and not unreleased" \
  --max-depth 200 \
  -T svg:cairo:gd \
  -O \
  -s 72 \
  -v
