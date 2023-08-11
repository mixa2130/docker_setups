#!/usr/bin/env python

import sys


for line in sys.stdin:
    try:
        print >> sys.stderr, "reporter:counter:Custom,All words,{}".format(1)
        key, value = line.strip().split('\t', 1)
        key = 99999 - int(key)
    except ValueError as e:
        print >> sys.stderr, "reporter:counter:Custom,Invalid words,{}".format(1)
        continue
    print "%s\t%s" % (value, key)

