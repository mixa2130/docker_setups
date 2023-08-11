#! /usr/bin/env python3

import random
import sys

sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')

for line in sys.stdin:
    x, y = map(float, line.strip().split())
    is_inside = 1 if (x * x + y * y <= 1) else 0
    print("{}\t{}".format(is_inside, 1))
