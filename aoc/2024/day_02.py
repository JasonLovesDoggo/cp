from typing import List
import aoc_helper
from aoc_helper import list, map, range


def parse_raw(raw: str):
    return raw

def check_report_safety(report: List[int]) -> bool:
    # Determine initial trend
    if len(report) < 2:
        return False

    increasing = report[1] > report[0]

    for idx in range(1, len(report)):
        # Check delta conditions
        delta = report[idx] - report[idx - 1]

        # Validate magnitude and trend
        if not (0 < abs(delta) <= 3):
            return False

        if increasing and delta < 0:
            return False

        if not increasing and delta > 0:
            return False

    return True

def part_one(data=None):
    if data is None:
        data = aoc_helper.fetch(2, 2024)

    N_safe = 0

    for report_line in data.splitlines():
        report = list(map(int, report_line.split()))

        if check_report_safety(report):
            N_safe += 1

    return N_safe

def part_two(data=None):
    if data is None:
        data = aoc_helper.fetch(2, 2024)

    N_safe = 0

    for report_line in data.splitlines():
        report = list(map(int, report_line.split()))

        # Check if report is safe without removing any level
        if check_report_safety(report):
            N_safe += 1
        else:
            # Try removing each level and check if it becomes safe
            for i in range(len(report)):
                temp_report = report[:i] + report[i + 1:]
                if check_report_safety(temp_report):
                    N_safe += 1
                    break

    return N_safe

# Main execution
if __name__ == '__main__':
    raw = aoc_helper.fetch(2, 2024)
    data = parse_raw(raw)

    aoc_helper.lazy_test(day=2, year=2024, parse=parse_raw, solution=part_one)
    aoc_helper.lazy_test(day=2, year=2024, parse=parse_raw, solution=part_two)

    aoc_helper.lazy_submit(day=2, year=2024, solution=part_one, data=data)
    aoc_helper.lazy_submit(day=2, year=2024, solution=part_two, data=data)
