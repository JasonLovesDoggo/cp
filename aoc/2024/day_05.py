import functools
from collections import defaultdict

import aoc_helper

raw = aoc_helper.fetch(5, 2024)


def parse_raw(raw: str):
    sections = raw.strip().split('\n\n')
    rules = []
    for line in sections[0].split('\n'):
        before, after = map(int, line.split('|'))
        rules.append((before, after))
    updates = []
    for line in sections[1].split('\n'):
        updates.append(list(map(int, line.split(','))))
    return rules, updates

def is_valid_order(update, rules):
    for x, y in rules:
        if x in update and y in update:
            x_index = update.index(x)
            y_index = update.index(y)
            if x_index > y_index:
                return False
    return True

def part_one(data=None):
    rules, updates = data
    middle_page_sum = 0
    for update in updates:
        if is_valid_order(update, rules):
            middle_page = update[len(update) // 2]
            middle_page_sum += middle_page
    return middle_page_sum

aoc_helper.lazy_test(day=5, year=2024, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=5, year=2024, solution=part_one, data=raw)

def part_two(raw):
    sections = raw.strip().split('\n\n')
    rules = []
    for line in sections[0].split('\n'):
        before, after = map(int, line.split('|'))
        rules.append((before, after))
    updates = []
    for line in sections[1].split('\n'):
        updates.append(list(map(int, line.split(','))))

    def is_valid_order(update):
        for x, y in rules:
            if x in update and y in update:
                x_index = update.index(x)
                y_index = update.index(y)
                if x_index > y_index:
                    return False
        return True

    def correct_order(update):
        corrected = update.copy()
        while True:
            changed = False
            for x, y in rules:
                if x in corrected and y in corrected and corrected.index(x) > corrected.index(y):
                    corrected.remove(x)
                    corrected.insert(corrected.index(y), x)
                    changed = True
            if not changed:
                break
        return corrected

    middle_page_sum = 0
    for update in updates:
        if not is_valid_order(update):
            corrected_update = correct_order(update)
            middle_page = corrected_update[len(corrected_update) // 2]
            middle_page_sum += middle_page
    return middle_page_sum

aoc_helper.lazy_test(day=5, year=2024, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=5, year=2024, solution=part_two, data=raw)
