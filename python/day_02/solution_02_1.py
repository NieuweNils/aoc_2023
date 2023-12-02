import os

import requests
from dotenv import load_dotenv
from typing import List
import re

DAY = 2

RED_COUNT_REGEX = r'\d+(?=\s+red)'
BLUE_COUNT_REGEX = r'\d+(?=\s+blue)'
GREEN_COUNT_REGEX = r'\d+(?=\s+green)'

MAX_DICE = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def load_data() -> List[str]:
    load_dotenv()
    session_cookie = os.getenv("session_cookie")
    auth_header = {"Cookie": f"session={session_cookie}"}
    url = f"https://adventofcode.com/2023/day/{DAY}/input"

    return [line for line in requests.get(headers=auth_header, url=url).iter_lines(decode_unicode=True)]


def find_valid_game_ids(data: List[str]) -> set:
    game_validity = {"all_games": set(), "invalid_games": set()}
    for line in data:
        game_id = int(line.split(":")[0][5:])
        game_validity["all_games"].add(game_id)

        game_data = line.split(":")[1]
        red = [int(entry) for entry in re.findall(pattern=RED_COUNT_REGEX, string=game_data)]
        blue = [int(entry) for entry in re.findall(pattern=BLUE_COUNT_REGEX, string=game_data)]
        green = [int(entry) for entry in re.findall(pattern=GREEN_COUNT_REGEX, string=game_data)]
        if max(red) > MAX_DICE["red"] or max(blue) > MAX_DICE["blue"] or max(green) > MAX_DICE["green"]:
            game_validity["invalid_games"].add(game_id)

    game_validity["valid_games"] = game_validity["all_games"] - game_validity["invalid_games"]

    return game_validity["valid_games"]


def main():
    data = load_data()
    valid_game_ids = find_valid_game_ids(data)
    answer = sum(valid_game_ids)
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
