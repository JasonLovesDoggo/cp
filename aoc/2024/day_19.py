from collections import Counter, defaultdict, deque

import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
    decode_text,
    extract_ints,
    extract_iranges,
    extract_ranges,
    extract_uints,
    frange,
    irange,
    iter,
    list,
    map,
    multirange,
    range,
    search,
    tail_call,
)

raw = aoc_helper.fetch(19, 2024)


def parse_raw(raw: str):
    return raw


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data): ...


aoc_helper.lazy_test(day=19, year=2024, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data): ...


aoc_helper.lazy_test(day=19, year=2024, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=19, year=2024, solution=part_one, data=data)
aoc_helper.lazy_submit(day=19, year=2024, solution=part_two, data=data)
