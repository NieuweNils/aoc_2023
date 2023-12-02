import os
import re
from typing import List

import requests
from dotenv import load_dotenv

DAY = 1

WORD_TO_NUMBER = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    # "zero": "0"
}


def load_data() -> List[str]:
    load_dotenv()
    session_cookie = os.getenv("SESSION_COOKIE")
    auth_header = {"Cookie": f"session={session_cookie}"}
    url = f"https://adventofcode.com/2023/day/{DAY}/input"

    return [line for line in requests.get(headers=auth_header, url=url).iter_lines(decode_unicode=True)]


def extract_numbers(data: List[str]) -> List[List[str]]:
    output = []
    regex_pattern = r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))'
    for line in data:
        numbers = re.findall(regex_pattern, line)
        output.append(numbers)
    return output


def convert_words_to_numbers(numbers: List[List[str]]) -> List[List[str]]:
    output = []
    for line in numbers:
        mapped_line = [WORD_TO_NUMBER[number] if len(number) > 1 else number for number in line]
        output.append(mapped_line)
    return output


def combine_first_last_digit(digits: List[List[str]]) -> List[int]:
    output = []
    for line in digits:
        first_digit = line[0]
        last_digit = line[-1]
        total_number = int(first_digit + last_digit)
        output.append(total_number)
    return output


def main():
    data = load_data()
    numbers = extract_numbers(data)
    digits = convert_words_to_numbers(numbers)
    calibration_values = combine_first_last_digit(digits)
    answer = sum(calibration_values)
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
