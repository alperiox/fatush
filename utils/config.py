# modify the config
import os
import yaml

CWD = os.getcwd()
CONFIG_PATH = os.path.join(CWD, "config.yaml")

def add_config(key, value):
    conf = load_config()
    conf[key] = value

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(conf, f)

def remove_config(key, value):
    conf = load_config()
    conf.pop(key)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config

def create_config():
    with open(CONFIG_PATH, "w") as f:
        # dump an empty dictionary
        yaml.dump({}, f)
