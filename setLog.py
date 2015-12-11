import logging
from logging.config import dictConfig
import yaml

def _log(path):
    with open('logging.yaml', 'rt') as f:
        config = yaml.load(f.read())
    config['handlers']['info_file_handler']['filename'] = '%s.log' % path
    config['handlers']['error_file_handler']['filename'] = '%s.err' % path
    dictConfig(config)
    logger = logging.getLogger(__name__)
    return(logger)

