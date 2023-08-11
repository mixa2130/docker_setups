#! /usr/bin/env python3

import sys

DEBUG = 0

sum_inside = 0
sum_cnt = 0
if DEBUG:
    stdin = open('../sort_result').readlines()
for line in stdin if DEBUG else sys.stdin:
    flag, cnt = map(int, line.strip().split())
    sum_inside += flag
    sum_cnt += cnt

print("{}\t{}".format(4 * sum_inside, sum_cnt))
