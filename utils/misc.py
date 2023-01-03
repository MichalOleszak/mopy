from datetime import datetime


def split_list_into_sublists_of_size_n(lst, n):
    """
    input = [1, 2, 3, 4, 5, 6, 7, 8]
    output = split_list_into_sublists_of_size_n(input, 3)
    >> [[1, 2, 3], [4, 5, 6], [7, 8]]
    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def multi_replace(stringlike, pettern_to_replacement_dict):
    """
    Replace multiple pattern with corresponding replacements
    """
    string = str(stringlike)
    for pattern, replacement in pettern_to_replacement_dict.items():
        string = string.replace(pattern, replacement)
    return string


def get_current_timestamp_as_pretty_string(precision="minutes"):
    """
    Output format: '2022_04_05-12_19_58'
    """
    if precision == "minutes":
        cutoff = 16
    elif precision == "seconds":
        cutoff = 19
    else:
        raise ValueError("'precision' should be one of: 'minutes', 'seconds'")
    return multi_replace(datetime.now(), {"-": "_", ":": "_", " ": "-"})[:cutoff]
