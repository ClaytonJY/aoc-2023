import operator
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Self

EXAMPLE: list[str] = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip().split("\n")


@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __contains__(self, other: Self) -> bool:
        """
        >>> CubeSet(red=1, green=2, blue=6) in CubeSet(red=2, green=3, blue=6)
        True
        >>> CubeSet(red=1, green=2, blue=6) in CubeSet(red=2, green=1, blue=6)
        False
        """
        return all(
            getattr(self, color) >= getattr(other, color)
            for color in self.__annotations__
        )

    def __or__(self, other: Self) -> Self:
        """
        >>> CubeSet(red=1, green=2, blue=6) | CubeSet(red=2, green=3, blue=6)
        CubeSet(red=2, green=3, blue=6)
        """
        return self.__class__(
            **{
                color: max(getattr(self, color), getattr(other, color))
                for color in self.__annotations__
            }
        )

    def power(self) -> int:
        """
        >>> CubeSet(red=1, green=2, blue=6).power()
        12
        """
        return reduce(
            operator.mul, (getattr(self, color) for color in self.__annotations__)
        )

    @classmethod
    def from_text(cls, text: str) -> Self:
        """
        >>> CubeSet.from_text('1 red, 2 green, 6 blue')
        CubeSet(red=1, green=2, blue=6)
        """
        input: dict[str, int] = {}
        for part in text.split(", "):
            count, color = part.split(" ")
            input[color] = int(count)
        return cls(**input)


@dataclass
class Game:
    id: int
    hands: list[CubeSet]

    @classmethod
    def from_line(cls, line: str) -> Self:
        """
        >>> Game.from_line('Game 1: 3 blue, 4 red; 2 green')
        Game(id=1, hands=[CubeSet(red=4, green=0, blue=3), CubeSet(red=0, green=2, blue=0)])
        """
        game_str, hands_str = line.split(": ")
        id = int(game_str.split(" ")[1])
        hands = [CubeSet.from_text(hand_str) for hand_str in hands_str.split("; ")]
        return cls(id=id, hands=hands)


def part1(lines: list[str]) -> int:
    """
    >>> part1(EXAMPLE)
    8
    """
    bag = CubeSet(red=12, green=13, blue=14)
    games: list[Game] = [Game.from_line(line) for line in lines]

    return sum(game.id for game in games if all(hand in bag for hand in game.hands))


def part2(lines: list[str]) -> int:
    """
    >>> part2(EXAMPLE)
    2286
    """
    games: list[Game] = [Game.from_line(line) for line in lines]

    return sum(reduce(operator.or_, game.hands).power() for game in games)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    lines = Path("inputs/day2.txt").read_text().strip().split("\n")

    assert part1(lines) == 2810
    assert part2(lines) == 69110
