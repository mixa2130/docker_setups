#! /usr/bin/env python

import random
import sys

key = 0
inside = 0
outside = 0

for line in sys.stdin:
    x, y = map(float, line.strip().split())
    if (x * x + y * y <= 1):
        print >> sys.stderr, "reporter:counter:Wiki stats,Total words,1"
    else:
        print >> sys.stderr, "reporter:counter:pi,outside,1"
    print("{}\t{}".format(is_inside, 1))
