#! /usr/bin/env python3

import sys

sum_inside = 0
sum_count = 0

for line in sys.stdin:
	try:
		is_inside, count = map(int, line.strip().split('\t'))
	except ValueError:
		continue
	sum_inside += is_inside
	sum_count += count

print("{}\t{}".format(4 * sum_inside, sum_count))
