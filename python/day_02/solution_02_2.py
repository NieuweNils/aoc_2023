import os

import requests
from dotenv import load_dotenv
from typing import List
import re

DAY = 2

RED_COUNT_REGEX = r'\d+(?=\s+red)'
BLUE_COUNT_REGEX = r'\d+(?=\s+blue)'
GREEN_COUNT_REGEX = r'\d+(?=\s+green)'


def load_data() -> List[str]:
    load_dotenv()
    session_cookie = os.getenv("session_cookie")
    auth_header = {"Cookie": f"session={session_cookie}"}
    url = f"https://adventofcode.com/2023/day/{DAY}/input"

    return [line for line in requests.get(headers=auth_header, url=url).iter_lines(decode_unicode=True)]


def find_smallest_cube_sets(data: List[str]) -> List[tuple]:
    smallest_sets = []
    for line in data:
        game_data = line.split(":")[1]
        red = [int(entry) for entry in re.findall(pattern=RED_COUNT_REGEX, string=game_data)]
        blue = [int(entry) for entry in re.findall(pattern=BLUE_COUNT_REGEX, string=game_data)]
        green = [int(entry) for entry in re.findall(pattern=GREEN_COUNT_REGEX, string=game_data)]
        sufficient_red, sufficient_blue, sufficient_green = max(red), max(blue), max(green)
        smallest_cube_set = (sufficient_red, sufficient_blue, sufficient_green)
        smallest_sets.append(smallest_cube_set)

    return smallest_sets


def power_of_set(smallest_cube_sets: List[tuple]) -> List[tuple]:
    powers = []
    for cube_set in smallest_cube_sets:
        power = cube_set[0] * cube_set[1] * cube_set[2]
        powers.append(power)
    return powers


def main():
    data = load_data()
    smallest_cube_sets = find_smallest_cube_sets(data)
    powers_of_cube_sets = power_of_set(smallest_cube_sets)
    answer = sum(powers_of_cube_sets)
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
