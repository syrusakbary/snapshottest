import re


def update_path(current_path, key_or_index, is_dict=False):
    if is_dict:
        if current_path == "":
            return key_or_index
        return "{}.{}".format(current_path, key_or_index)
    else:
        return "{}[{}]".format(current_path, key_or_index)


def clear_ignore_keys(data, ignore_keys, current_path=""):
    if isinstance(data, dict):
        for key, value in data.items():
            temp_path = update_path(current_path, key, is_dict=True)
            matched = match_ignored_key(key, data, ignore_keys, temp_path)
            if not matched:
                data[key] = clear_ignore_keys(value, ignore_keys, temp_path)
        return data
    elif isinstance(data, list):
        for index, value in enumerate(data):
            temp_path = update_path(current_path, index)
            matched = match_ignored_key(index, data, ignore_keys, temp_path)
            if not matched:
                data[index] = clear_ignore_keys(value, ignore_keys, temp_path)
        return data
    elif isinstance(data, tuple):
        return tuple(
            clear_ignore_keys(value, ignore_keys, update_path(current_path, index))
            for index, value in enumerate(data)
        )
    return data


def match_ignored_key(key_or_index, data, ignore_keys, temp_path):
    for ignored in ignore_keys:
        escaped = ignored.translate(str.maketrans({"[": r"\[", "]": r"\]"}))
        if re.match("{}$".format(escaped), temp_path):
            data[key_or_index] = None
            return True
    return False
