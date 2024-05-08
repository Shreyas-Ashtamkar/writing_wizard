from functools import cache
from .read_yaml_config import _read_config

@cache
def get_configs(filename="config.yaml"):
    try:
        configs = _read_config(filename)
    except Exception as e:
        print("error : get_configs : 7 :", e.__str__())
        configs = None
    finally:
        return configs
