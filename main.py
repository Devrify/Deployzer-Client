import argparse
import logging
import os
from logging.config import fileConfig
from config.logging_config import *

if __name__ == '__main__':
    print(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
    # 初始化 logger
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging_config.ini'))
    logger = logging.getLogger(__name__)

    # 从命令行获取参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
       '-u', '--url',
        dest='url', type=str, help='Server url.Could be ip address or hostname', required=True)
    parser.add_argument(
       '-t' ,'--token',
        dest='token', type=str, help='Optional Server token.', required=False)
    args = parser.parse_args()
    logger.error(str(args))
    init_logger()