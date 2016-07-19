# @andric 2016
"""
Created to log things easily.

Taken much from
http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
"""
import logging
from logging.config import dictConfig
import yaml


def setup_log(path):
    """Made to ease logging."""
    with open('logging.yaml', 'rt') as yamf:
        config = yaml.load(yamf.read())
    config['handlers']['info_file_handler']['filename'] = '%s.log' % path
    config['handlers']['error_file_handler']['filename'] = '%s.err' % path
    dictConfig(config)
    logger = logging.getLogger(__name__)
    return logger
