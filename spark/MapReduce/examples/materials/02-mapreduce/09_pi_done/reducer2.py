import sys

sys.stdin = open(sys.stdin.fileno(), encoding='utf-8')


sum_inside = 0
sum_count = 0

for line in sys.stdin:
	try:
		is_inside, count = line.strip().split()[-2:]
		is_inside = int(is_inside)
		count = int(count)
	except ValueError:
		continue
	sum_inside += is_inside
	sum_count += count

print('{}\t{}'.format(sum_inside, sum_count))

