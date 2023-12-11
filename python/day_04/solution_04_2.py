import os
from queue import Queue
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


def create_card_process_job(line: str, q: Queue, card_id: int, cards_to_copy: dict) -> None:
    _, cards = line.split(sep=":")  # take of the "Card XX:
    winning, mine = cards.split("|")

    winning_set = set(winning.split())
    mine_set = set(mine.split())

    overlap = winning_set.intersection(mine_set)
    copies = len(overlap)
    cards_to_copy[card_id] = copies

    q.put(card_id)


def main():
    data = load_data()
    cards = 0
    queue = Queue()
    cards_to_copy = {}
    # initialise the queue and #copies for all cards once to start off with
    [create_card_process_job(card_data, queue, card_id, cards_to_copy) for card_id, card_data in enumerate(data)]

    # process the queue
    while not queue.empty():
        cards += 1
        card_id = queue.get()
        # create a copy the job of the cards following the current one, one for each winning number in the scratchcard
        for i in range(card_id + 1, card_id + cards_to_copy[card_id] + 1):
            queue.put(i)

    answer = cards
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
