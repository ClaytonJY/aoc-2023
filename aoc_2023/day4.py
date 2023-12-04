import re
from dataclasses import dataclass
from pathlib import Path
from typing import Self

EXAMPLE = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".strip().split("\n")


@dataclass
class Card:
    numbers: set[int]
    winners: set[int]

    def n_winners(self) -> int:
        return len(self.numbers.intersection(self.winners))

    def score(self) -> int:
        """
        >>> Card(numbers={12, 13}, winners={24, 25}).score()
        0
        >>> Card(numbers={1, 2, 3}, winners={2, 4}).score()
        1
        >>> Card(numbers={1, 2, 3}, winners={2, 3, 4}).score()
        2
        >>> Card(numbers={1, 2, 3}, winners={1, 2, 3, 4}).score()
        4
        """
        n_winners = self.n_winners()
        return 2 ** (n_winners - 1) if n_winners else 0

    @classmethod
    def from_line(cls, line: str) -> Self:
        """
        >>> Card.from_line('Card 1: 12 13 | 24 25')
        Card(numbers={12, 13}, winners={24, 25})
        """
        numbers, winners = line.split(": ")[1].split(" | ")

        return cls(
            numbers={int(x.group(0)) for x in re.finditer("[0-9]+", numbers)},
            winners={int(x.group(0)) for x in re.finditer("[0-9]+", winners)},
        )


def solution(lines: list[str]) -> tuple[int, int]:
    """
    >>> solution(EXAMPLE)
    (13, 30)
    """
    part1 = 0

    cards: list[Card] = []
    for card in (Card.from_line(line) for line in lines):
        part1 += card.score()
        cards.append(card)

    counts = [1 for _ in range(len(cards))]

    for i in range(len(cards)):
        for j in range(i + 1, i + 1 + cards[i].n_winners()):
            counts[j] += counts[i]

    part2 = sum(counts)

    return (part1, part2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    lines = Path("inputs/day4.txt").read_text().strip().split("\n")

    part1, part2 = solution(lines)
    assert part1 == 28538
    assert part2 == 9425061
