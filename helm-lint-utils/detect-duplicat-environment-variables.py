import sys
from collections import Counter

from utils import get_concatenated_yaml


class DuplicateKeysError(Exception):
    pass


def try_find_duplicate_keys_in_env(yaml_data):
    env_key = get_inner_key(yaml_data, "env")
    names_counter = Counter(_["name"] for _ in env_key)
    duplicates = [(key, count) for (key, count) in names_counter.items() if count > 1]
    if len(duplicates) > 0:
        raise DuplicateKeysError(f"Found duplicate {duplicates}")


def get_inner_key(obj, inner_key):
    if type(obj) is not dict and type(obj) is not list:
        raise KeyError(f"Did not find key: {inner_key}")
    elif type(obj) is dict:
        if inner_key in obj:
            return obj.get(inner_key)
        for key in obj:
            try:
                return get_inner_key(obj.get(key), inner_key)
            except KeyError:
                continue
    elif type(obj) is list:
        for entry in obj:
            try:
                return get_inner_key(entry, inner_key)
            except KeyError:
                continue
    raise KeyError(f"Did not find key: {inner_key}")

def main():
    concatenated_yaml = get_concatenated_yaml()
    did_find_duplicate_keys = False
    for yaml_file in concatenated_yaml:
        try:
            try_find_duplicate_keys_in_env(yaml_file)
            print("Did not find duplicates here.")
        except DuplicateKeysError as e:
            did_find_duplicate_keys = True
            print(e)
        except Exception as e:
            print(e)
    sys.exit(int(did_find_duplicate_keys))
    
if "__main__" == __name__:
    main()
