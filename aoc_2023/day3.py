from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Generator, Self

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
    value: str
    start: int

    def __len__(self) -> int:
        """
        >>> len(Element("*", 0))
        1
        >>> len(Element("12", 0))
        2
        """
        return len(str(self.value))

    def is_number(self) -> bool:
        """
        >>> Element("*", 0).is_number()
        False
        >>> Element("12", 0).is_number()
        True
        """
        return self.value.isdigit()

    @cached_property
    def end(self) -> int:
        """
        >>> Element("*", 0).end
        1
        >>> Element(12, 0).end
        2
        """
        return self.start + len(self)

    def __matmul__(self, other: Self) -> bool:
        """
        >>> Element("*", 0) @ Element("*", 0)
        True
        >>> Element("*", 1) @ Element("*", 0)
        True
        >>> Element(12, 0) @ Element("*", 1)
        True
        >>> Element(12, 0) @ Element("*", 2)
        True
        >>> Element("*", 2) @ Element(12, 0)
        True
        >>> Element("12", 0) @ Element("*", 3)
        False
        >>> Element("*", 3) @ Element("12", 0)
        False
        """
        distance = max(other.start - self.end, self.start - other.end)
        return distance < 1


@dataclass
class Schematic:
    elements: list[list[Element]]

    def part_numbers(self) -> Generator[int, None, None]:
        """
        >>> list(Schematic.from_lines(["467..114..", "...*......"]).part_numbers())
        [467]
        """
        for i, row in enumerate(self.elements):
            for element in row:
                if element.is_number() and self.adjacent_to_symbol(element, i):
                    yield int(element.value)

    def adjacent_to_symbol(self, element: Element, row_idx: int) -> bool:
        row_idxs = (
            x for x in range(row_idx - 1, row_idx + 2) if 0 <= x < len(self.elements)
        )
        symbols = (
            element
            for x in row_idxs
            for element in self.elements[x]
            if not element.is_number()
        )
        for symbol in symbols:
            if element @ symbol:
                return True
        return False

    @staticmethod
    def parse_line(line: str) -> list[Element]:
        """
        >>> Schematic.parse_line("467..114..")
        [Element(value='467', start=0), Element(value='114', start=5)]
        >>> Schematic.parse_line(".**..!*?..")
        [Element(value='**', start=1), Element(value='!*?', start=5)]
        >>> Schematic.parse_line("617*......")
        [Element(value='617', start=0), Element(value='*', start=3)]
        >>> Schematic.parse_line("..-123")
        [Element(value='-', start=2), Element(value='123', start=3)]
        """
        elements: list[Element] = []
        buffer = ""
        for i, char in enumerate(line):
            if char == ".":
                if buffer:
                    elements.append(Element(buffer, i - len(buffer)))
                    buffer = ""
            elif char.isdigit() == buffer.isdigit():
                buffer += char
            else:
                if buffer:
                    elements.append(Element(buffer, i - len(buffer)))
                buffer = char
        if buffer:
            elements.append(Element(buffer, i - len(buffer) + 1))
        return elements

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        """
        >>> Schematic.from_lines(["467..114..", "...*......"]).elements
        [[Element(value='467', start=0), Element(value='114', start=5)], [Element(value='*', start=3)]]
        """
        return cls(elements=[list(cls.parse_line(line)) for line in lines])


def part1(lines: list[str]) -> int:
    """
    >>> part1(EXAMPLE)
    4361
    """
    schematic = Schematic.from_lines(lines)
    return sum(schematic.part_numbers())


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

    print(part1(lines))
    print(part2(lines))
