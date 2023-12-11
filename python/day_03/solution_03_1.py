import os
import re
from collections import deque
from typing import List, Deque

import requests
from dotenv import load_dotenv

DAY = 3

SYMBOL_REGEX = '[^.\w]'
DIGITS_REGEX = '\d+'

"""
All the comments are generated using CoPilot. I am not so sure I like it. It is a bit too verbose for my liking. 
(funnily enough, this comment was also generated using CoPilot) 
"""


def load_data() -> List[str]:
    load_dotenv()
    session_cookie = os.getenv("SESSION_COOKIE")
    auth_header = {"Cookie": f"session={session_cookie}"}
    url = f"https://adventofcode.com/2023/day/{DAY}/input"

    return [line for line in requests.get(headers=auth_header, url=url).iter_lines(decode_unicode=True)]


def contains_symbol(matrix: List[str]) -> List[int]:
    """
    This function checks if the matrix contains a symbol.
    :param matrix: a matrix of strings
    :return: a boolean indicating whether the matrix contains a symbol
    """
    for row in matrix:
        if re.findall(pattern=SYMBOL_REGEX, string=row):
            return True
    return False


def construct_neighbour_matrix(matrix: Deque[str], start: int, end: int):
    """
    This function constructs a smaller matrix of the lines in the last_three_lines around the number that is present between start and end.
    :param matrix: a matrix of strings
    :param start: the start index of the number
    :param end: the end index of the number
    :return: a matrix  which is a subset of matrix that contains the lines in matrix that are around the number between start and end
    """
    if start == 0:
        start = 1
    neighbour_matrix = [r[start - 1:end + 1] for r in matrix]
    return neighbour_matrix


def add_relevant_numbers_in_line(relevant_numbers: List[int], last_three_lines: Deque[str], line_to_query: int) \
        -> List[int]:
    """
    This looks through the line_to_query and calls contains_symbol to see if there is a symbol in the matrix around the number.
    :param relevant_numbers: the running total of relevant numbers
    :param last_three_lines: the last three lines of the data
    :param line_to_query: the line to query
    :return: the updated relevant_numbers list
    """
    number_indices_line = [(match.start(), match.end()) for match in
                           re.finditer(pattern=DIGITS_REGEX, string=last_three_lines[line_to_query])]
    for start, end in number_indices_line:
        neighbour_matrix = construct_neighbour_matrix(matrix=last_three_lines, start=start, end=end)
        if contains_symbol(matrix=neighbour_matrix):
            number = int(last_three_lines[line_to_query][start: end])
            relevant_numbers.append(number)
    return relevant_numbers


def find_relevant_numbers(data: List[str]) -> List[int]:
    """
    This function loops through each line in the data and calls add_relevant_numbers_in_line to find the relevant numbers for that line.
    :param data: input data for today's puzzle
    :return: a list of all numbers that are next to a symbol
    """
    relevant_numbers = []
    last_three_lines = deque(maxlen=3)
    # do first through second-to-last lines
    for line in data:
        last_three_lines.append(line)
        if len(last_three_lines) < 2:
            continue
        relevant_numbers = add_relevant_numbers_in_line(relevant_numbers, last_three_lines, line_to_query=-2)
    # do last line
    relevant_numbers = add_relevant_numbers_in_line(relevant_numbers, last_three_lines, line_to_query=-1)

    return relevant_numbers


def main():
    data = load_data()
    relevant_numbers = find_relevant_numbers(data)
    answer = sum(relevant_numbers)
    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
