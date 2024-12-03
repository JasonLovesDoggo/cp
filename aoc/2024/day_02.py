from typing import List

import aoc_helper
from aoc_helper import (
    list,
    map,
    range,
)

raw = aoc_helper.fetch(2, 2024)


def parse_raw(raw: str):
    return raw

data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    N_safe = 0
    for report in data.splitlines():
        report: List[int] = list(map(int, report.split()))
        increasing = False
        is_safe = False
        for idx, record in enumerate(report):
            if idx == 0: # Set increasing/decreasing
                if report[1] > report[0]:
                    increasing = True
                else:
                    increasing = False
                continue
            delta_good = record > report[idx - 1] if increasing else record < report[idx - 1]
            if 0 < abs(record - report[idx - 1]) <= 3 and delta_good:
                is_safe = True
                continue
            else:
                is_safe = False
                break
        if is_safe:
            N_safe += 1

    return N_safe





aoc_helper.lazy_test(day=2, year=2024, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    N_safe = 0
    for report in data.splitlines():
        report = list(map(int, report.split()))

        # Helper function to check if a report is safe
        def is_safe(report):
            increasing = None
            decreasing = None
            for i in range(1, len(report)):
                if increasing is None and decreasing is None:  # Initialize on the first check
                    increasing = report[i] > report[i - 1]
                    decreasing = report[i] < report[i - 1]
                if not (0 < abs(report[i] - report[i - 1]) <= 3 and
                        (increasing and report[i] > report[i - 1] or  # Check increasing
                         decreasing and report[i] < report[i - 1])):  # Check decreasing
                    return False
            return True

        if is_safe(report):  # Check if safe without removing any level
            N_safe += 1
        else:
            # Try removing each level and check if it becomes safe
            for i in range(len(report)):
                temp_report = report[:i] + report[i + 1:]
                if is_safe(temp_report):
                    N_safe += 1
                    break

    return N_safe



aoc_helper.lazy_test(day=2, year=2024, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=2, year=2024, solution=part_one, data=data)
aoc_helper.lazy_submit(day=2, year=2024, solution=part_two, data=data)
