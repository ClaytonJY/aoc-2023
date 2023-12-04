import re
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Generator, Iterable, Self

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


@dataclass
class Element:
    text: str
    start: int
    end: int

    def adjacent(self, other: Self) -> bool:
        return (self.start <= other.end) and (other.start <= self.end)

    def is_number(self) -> bool:
        return self.text.isdigit()

    @classmethod
    def from_match(cls, match: re.Match) -> Self:
        return cls(match.group(0), match.start(), match.end())


def elements(line: str) -> Generator[Element, None, None]:
    return (
        Element.from_match(match) for match in re.finditer("([0-9]+|[^0-9.]+)", line)
    )


def numbers(elements: Iterable[Element]) -> Generator[Element, None, None]:
    return (element for element in elements if element.is_number())


def symbols(elements: Iterable[Element]) -> Generator[Element, None, None]:
    return (element for element in elements if not element.is_number())


def part1(lines: list[str]) -> int:
    """
    >>> part1(EXAMPLE)
    4361
    """
    total = 0

    lasts: list[Element] = []
    currents: list[Element] = []
    for line in lines:
        for element in elements(line):
            if element.is_number():
                # look at recent symbols
                for symbol in symbols(chain(lasts, currents)):
                    if element.adjacent(symbol):
                        total += int(element.text)
                        break
                else:
                    # only add to currents if we didn't add to total
                    currents.append(element)
            else:
                # look at recent numbers
                for number in numbers(chain(lasts, currents)):
                    if element.adjacent(number):
                        total += int(number.text)
                        # seems I should remove duplicates,
                        # but what I've tried lowers the total

                # add to current regardless of adjacent numbers found
                currents.append(element)

        # move currents to lasts and clear currents
        lasts = currents
        currents = []

    return total


@dataclass
class GearRatio:
    a: Element
    asterisk: Element
    b: Element | None = None

    def value(self) -> int | None:
        return int(self.a.text) * int(self.b.text) if self.b else None


def part2(lines: list[str]) -> int:
    """
    >>> part2(EXAMPLE)
    467835
    """
    schematic = [list(elements(line)) for line in lines]
    total = 0

    for i, row in enumerate(schematic):
        for element in row:
            partial_ratio: int | None = None
            if element.text == "*":
                for number in (
                    number
                    for x in range(max(0, i - 1), min(len(schematic), i + 2))
                    for number in numbers(schematic[x])
                ):
                    if element.adjacent(number):
                        if partial_ratio:
                            total += partial_ratio * int(number.text)
                            break
                        else:
                            partial_ratio = int(number.text)

    return total


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    lines = Path("inputs/day3.txt").read_text().strip().split("\n")

    assert part1(lines) == 507214
    print(part2(lines))
