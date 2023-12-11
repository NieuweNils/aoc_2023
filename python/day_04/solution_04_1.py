import os
from typing import List

import requests
from dotenv import load_dotenv

DAY = 4


def load_data() -> List[str]:
    load_dotenv()
    session_cookie = os.getenv("SESSION_COOKIE")
    auth_header = {"Cookie": f"session={session_cookie}"}
    url = f"https://adventofcode.com/2023/day/{DAY}/input"

    return [line for line in requests.get(headers=auth_header, url=url).iter_lines(decode_unicode=True)]


def score_card(line: str) -> int:
    _, cards = line.split(sep=":")  # take of the "Card XX:
    winning, mine = cards.split("|")

    winning_set = set(winning.split())
    mine_set = set(mine.split())

    overlap = winning_set.intersection(mine_set)
    if overlap:
        return 2 ** (len(overlap) - 1)
    return 0


def main():
    data = load_data()
    scores = [score_card(line) for line in data]
    answer = sum(scores)
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
