from pathlib import Path
import re


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


if __name__ == "__main__":
    lines = Path("inputs/day1.txt").read_text().strip().split("\n")
    print(Day1.part1(lines))
