def multi_replace(stringlike, pettern_to_replacement_dict):
    """
    Replace multiple pattern with corresponding replacements
    """
    string = str(stringlike)
    for pattern, replacement in pettern_to_replacement_dict.items():
        string = string.replace(pattern, replacement)
    return string
