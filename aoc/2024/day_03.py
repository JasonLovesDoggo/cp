import re

import aoc_helper
from aoc_helper import (
    extract_ints,
)

raw = aoc_helper.fetch(3, 2024)


def parse_raw(raw: str):
    return raw


data = parse_raw(raw)

# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    total = 0
    results = re.findall(r'(mul\([0-9]{1,3},[0-9]{1,3}\))', data)
    for result in results:
        ints = extract_ints(result)
        total += ints[0] * ints[1]
    return total



aoc_helper.lazy_test(day=3, year=2024, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    total = 0
    results = re.findall(r"(mul\([0-9]{1,3},[0-9]{1,3}\)|don't\(\)|do\(\))", data)
    ignore_result = False

    for result in results:
        if result == "don't()":
            ignore_result = True
            continue
        elif result == "do()":
            ignore_result = False
            continue
        if ignore_result:
            continue
        ints = extract_ints(result)
        total += ints[0] * ints[1]
    return total



aoc_helper.lazy_test(day=3, year=2024, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=3, year=2024, solution=part_one, data=data)
aoc_helper.lazy_submit(day=3, year=2024, solution=part_two, data=data)
