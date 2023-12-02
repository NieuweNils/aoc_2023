import os

import requests
from dotenv import load_dotenv
import re

DAY = 1


def main():
    load_dotenv()
    session_cookie = os.getenv("SESSION_COOKIE")
    auth_header = {"Cookie": f"session={session_cookie}"}
    url = f"https://adventofcode.com/2023/day/{DAY}/input"

    data = [line for line in requests.get(headers=auth_header, url=url).iter_lines(decode_unicode=True)]

    regex_pattern = r'\d'

    output_list = []
    for line in data:
        numbers_in_line = re.findall(regex_pattern, line)
        first_number = numbers_in_line[0]
        last_number = numbers_in_line[-1]
        total_number = int(first_number + last_number)
        output_list.append(total_number)

    answer = sum(output_list)
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
