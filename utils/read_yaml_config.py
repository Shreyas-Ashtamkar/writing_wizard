import yaml
from types import SimpleNamespace

def _recursive_namespace(d:dict):
    return SimpleNamespace(**{k: _recursive_namespace(v) if isinstance(v, dict) else v for k, v in d.items()})

def _read_config(filename):
    with open(filename, 'r') as file:
        return _recursive_namespace(yaml.safe_load(file))
