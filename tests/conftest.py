from logging import config
import yaml

with open("./tests/log_spec.yaml", "r") as log_spec_file:
    config.dictConfig(yaml.load(log_spec_file))
