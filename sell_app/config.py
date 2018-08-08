import yaml
import os


script_path = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_path, 'config.yml')
with open(config_file, 'r') as f:
    config = yaml.load(f)
    if config is None: raise Exception('Not found configure file.')
