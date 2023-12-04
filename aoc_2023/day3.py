import re
from itertools import chain
from pathlib import Path

EXAMPLE = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip().split("\n")


def part1(lines: list[str]) -> int:
    """
    >>> part1(EXAMPLE)
    4361
    """
    total = 0

    lasts: list[re.Match] = []
    currents: list[re.Match] = []
    for line in lines:
        for element in re.finditer("([0-9]+|[^0-9.]+)", line):
            if element.group(0).isdigit():
                # look at recent symbols
                for symbol in filter(
                    lambda x: not x.group(0).isdigit(), chain(lasts, currents)
                ):
                    if (element.start() <= symbol.end()) and (
                        symbol.start() <= element.end()
                    ):
                        # if adjacent, add to total
                        total += int(element.group(0))
                        break
                else:
                    # only add to currents if we didn't add to total
                    currents.append(element)
            else:
                # look at recent numbers
                for number in filter(
                    lambda x: x.group(0).isdigit(), chain(lasts, currents)
                ):
                    if (element.start() <= number.end()) and (
                        number.start() <= element.end()
                    ):
                        # add each to total and _remove_ so we don't double-count
                        total += int(number.group(0))
                        # seems I should remove duplicates,
                        # but what I've tried lowers the total

                # add to current regardless of adjacent numbers found
                currents.append(element)

        # move currents to lasts and clear currents
        lasts = currents
        currents = []

    return total


def part2(lines: list[str]) -> int:
    """
    >>> part2(EXAMPLE)
    0
    """
    return 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    lines = Path("inputs/day3.txt").read_text().strip().split("\n")

    assert part1(lines) == 507214
    # print(part2(lines))
