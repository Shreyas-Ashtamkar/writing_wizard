from functools import cache
from os import environ

from .read_yaml_config import _read_config
from .file_handling import write_to_file

from dotenv import load_dotenv

@cache
def get_configs(filename="config.yaml"):
    """Retrieve configurations from a YAML file.
    
    Args:
        filename (str): The name of the YAML file containing configurations. Defaults to "config.yaml".
    
    Returns:
        dict: A dictionary containing the configurations read from the YAML file, or None if an error occurs.
    """
    try:
        configs = _read_config(filename)
    except Exception as e:
        print("error : get_configs : 7 :", e.__str__())
        configs = None
    finally:
        return configs

def get_env(key):
    """Retrieve the value of the specified environment variable.
    
    Args:
        key (str): The key of the environment variable to retrieve.
    
    Returns:
        str: The value of the specified environment variable.
    """
    load_dotenv()
    return environ.get(key)

def set_env(key, value):
    """Set the environment variable with the specified key and value.
    
    Args:
        key (str): The key of the environment variable.
        value (str): The value to set for the environment variable.
    """
    environ[key] = value
