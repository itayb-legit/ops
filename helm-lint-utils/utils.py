import sys
import yaml


def get_concatenated_yaml():
    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        return list(yaml.load_all(f, yaml.loader.SafeLoader))