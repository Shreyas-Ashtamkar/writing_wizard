from functools import cache
from .read_yaml_config import _read_config
from .file_handling import write_to_file

from dotenv import load_dotenv
load_dotenv()

@cache
def get_configs(filename="config.yaml"):
    try:
        configs = _read_config(filename)
    except Exception as e:
        print("error : get_configs : 7 :", e.__str__())
        configs = None
    finally:
        return configs

def get_env(key):
    from os import environ
    return environ.get(key)
