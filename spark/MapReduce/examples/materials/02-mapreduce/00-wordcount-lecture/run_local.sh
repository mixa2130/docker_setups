#! /usr/bin/env bash

data="data/hobbit.txt"
cat $data | python3 ./mapper.py | sort | python3 ./reducer.py | sort -k2r | head
