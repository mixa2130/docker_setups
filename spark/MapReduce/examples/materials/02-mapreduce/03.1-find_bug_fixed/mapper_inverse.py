#!/usr/bin/env python

import sys


for line in sys.stdin:
    try:
        key, value = line.strip().split('\t', 1)
        value = 99999 - int(value)
    except ValueError as e:
        continue
    print "%s\t%s" % (value, key)

