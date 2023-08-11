#! /usr/bin/env python3

import sys

DEBUG = 0

if DEBUG:
    stdin = open('pi_points/part-0.0').readlines()
    stdout = open('../map_result', 'w')
for line in stdin if DEBUG else sys.stdin:
    x, y = map(float, line.strip().split())
    is_inside = 1 if (x * x + y * y <= 1) else 0
    if DEBUG:
        stdout.write("{}\t{}\n".format(is_inside, 1))
    else:
        print("{}\t{}".format(is_inside, 1))
