#!/usr/bin/env bash
python -m cProfile -o profile.cprof runtests.py
pyprof2calltree -k -i profile.cprof
