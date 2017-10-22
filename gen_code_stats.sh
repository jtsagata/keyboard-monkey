#!/bin/bash

cloc --exclude-dir=.idea --quiet --report-file=docs/code_stats.txt .
sed -i '1d' docs/code_stats.txt
cat docs/code_stats.txt
