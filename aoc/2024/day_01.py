import aoc_helper


raw = aoc_helper.fetch(1, 2024)


def parse_raw(raw: str):
    return raw


results = [[], []]

data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    for line in data.splitlines():
        one, two = line.split("   ")

        results[0].append(int(one))
        results[1].append(int(two))

    results[0] = sorted(results[0])
    results[1] = sorted(results[1])

    subresult = list(zip(results[0], results[1]))

    total_diff = 0

    for i in subresult:
        total_diff += abs(i[0] - i[1])

    return total_diff


aoc_helper.lazy_test(day=1, year=2024, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    total_similarity = 0
    for n in results[0]:
        total_similarity += n * results[1].count(n)

    return total_similarity


aoc_helper.lazy_test(day=1, year=2024, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=1, year=2024, solution=part_one, data=data)
aoc_helper.lazy_submit(day=1, year=2024, solution=part_two, data=data)
