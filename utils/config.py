# modify the config
import os
import yaml

CWD = os.getcwd()
CONFIG_PATH = os.path.join(CWD, "config.yaml")


def add_config(key, value, path=CONFIG_PATH):
    conf = load_config(path=path)
    conf[key] = value

    with open(path, "w") as f:
        yaml.dump(conf, f)


def remove_config(key, path=CONFIG_PATH):
    conf = load_config(path=path)
    conf.pop(key)


def load_config(path: str = CONFIG_PATH):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


def create_config(path: str = CONFIG_PATH):
    with open(path, "w") as f:
        # dump an empty dictionary
        yaml.dump({}, f)
