import re
import sys

from utils import get_concatenated_yaml

PORT_REGEX = re.compile(r".*[Pp]ort(s?)$")



def handle_file(yaml_file):
    entries = get_all_entries_by_key_regex(yaml_file, PORT_REGEX)
    first_error = None
    for entry in entries:
        try:
            ensure_entry_type_is_allowed(entry[1])
        except TypeError as e:
            first_error = first_error or e
            print(f"For key: '{entry[0]}' got error: {e}")
    if first_error is not None:
        raise first_error


def get_all_entries_by_key_regex(obj, regex: re.Pattern):
    result = []
    if type(obj) is not dict and type(obj) is not list:
        return result
    elif type(obj) is dict:
        for key in obj:
            if regex.match(key):
                result.append((key, obj.get(key)))
            result.extend(get_all_entries_by_key_regex(obj.get(key), regex))
    elif type(obj) is list:
        for entry in obj:
            result.extend(get_all_entries_by_key_regex(entry, regex))
    return result


def ensure_entry_type_is_allowed(entry):
    # Allow dict (nested object) type because some configurations has group a number of ports under a key with name port
    # presumably, the inner values that actually represent ports will also contain the name ports and will be caught as
    # separate entries.
    if type(entry) in (int, dict):
        return
    elif type(entry) is list:
        if len(entry) == 0 or type(entry[0]) in (int, dict, list):
            return
        raise TypeError(f"invalid type: list of {_get_printable_type(entry[0])}")
    raise TypeError(f"invalid type: {_get_printable_type(entry)}")


def _get_printable_type(obj):
    return type(obj).__name__

def main():
    concatenated_yaml = get_concatenated_yaml()
    did_find_non_int_ports = False
    for yaml_file in concatenated_yaml:
        try:
            handle_file(yaml_file)
            print("Did not find invalid value type for ports here")
        except TypeError:
            did_find_non_int_ports = True

    sys.exit(int(did_find_non_int_ports))

if __name__ == "__main__":
    main()
