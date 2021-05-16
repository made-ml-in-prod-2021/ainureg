import os
from pathlib import Path
import yaml
import logging
import logging.config


def setup_logging():
    """setup logging for all project"""
    conf_path = Path(__file__).parent.parent / "config" / "logging.conf.yml"
    assert os.path.isfile(conf_path)
    with open(conf_path) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin))
    logging.captureWarnings(True)
