def detect_conflict(dict1: dict, dict2: dict) -> bool:
    return any(key in dict2 and dict1[key] != dict2[key] for key in dict1)
