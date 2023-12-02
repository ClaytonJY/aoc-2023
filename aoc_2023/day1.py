import re
from pathlib import Path

WORD_TO_DIGIT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def first_digit(line: str) -> str:
    """
    >>> first_digit('two1nine')
    '2'
    >>> first_digit('eightwothree')
    '8'
    """
    if line[0].isdigit():
        return line[0]
    for word, digit in WORD_TO_DIGIT.items():
        if line.startswith(word):
            return digit
    return first_digit(line[1:])


def last_digit(line: str) -> str:
    """
    >>> last_digit('two1nine')
    '9'
    >>> last_digit('eightwothree')
    '3'
    >>> last_digit('threeightwo')
    '2'
    """
    if line[-1].isdigit():
        return line[-1]
    for word, digit in WORD_TO_DIGIT.items():
        if line.endswith(word):
            return digit
    return last_digit(line[:-1])


class Day1:
    @staticmethod
    def part1(lines: list[str]) -> int:
        """
        >>> lines = [
        ...     '1abc2',
        ...     'pqr3stu8vwx',
        ...     'a1b2c3d4e5f',
        ...     'treb7uchet'
        ... ]
        >>> Day1.part1(lines)
        142
        """
        pattern = re.compile("[^0-9]")
        numbers: list[int] = []
        for line in lines:
            digits: str = pattern.sub("", line)
            numbers.append(int(digits[0] + digits[-1]))

        return sum(numbers)

    @staticmethod
    def part2(lines: list[str]) -> int:
        """
        >>> lines = [
        ...     'two1nine',
        ...     'eightwothree',
        ...     'abcone2threexyz',
        ...     'xtwone3four',
        ...     '4nineeightseven2',
        ...     'zoneight234',
        ...     '7pqrstsixteen',
        ... ]
        >>> Day1.part2(lines)
        281
        """

        return sum(int(first_digit(line) + last_digit(line)) for line in lines)


if __name__ == "__main__":
    lines = Path("inputs/day1.txt").read_text().strip().split("\n")

    assert Day1.part1(lines) == 53080
    assert Day1.part2(lines) == 53268
