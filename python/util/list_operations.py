def flatten(nested_list: list) -> list:
    return [entry for sublist in nested_list for entry in sublist]
