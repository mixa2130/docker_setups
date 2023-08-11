#! /usr/bin/env python3

import sys

for line in sys.stdin:
    fields = line.strip().split('\t')
    fields[0] = fields[0].split('.')[0]
    print("\t".join(fields))
