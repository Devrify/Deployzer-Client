import argparse
import logging
import os
import time
from logging.config import fileConfig
from service.network_service import NetworkService
from service.executor_service import ExecutorService


if __name__ == '__main__':
    # 初始化 logger
    logging_config_file_path = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
    logging.config.fileConfig(logging_config_file_path)
    logger = logging.getLogger(__name__)

    # 从命令行获取参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
       '-u', '--url',
        dest='url', type=str, help='Server url.Could be ip address or hostname', required=True)
    parser.add_argument(
       '-t' ,'--token',
        dest='token', type=str, help='Optional server token.', required=True)
    parser.add_argument(
       '-n' ,'--name',
        dest='name', type=str, help='Optional client name.', required=False)
    args = parser.parse_args()

    # 初始化 http client
    logger.info('初始化 http client')
    http_client = NetworkService(args.url, args.token, args.name)
    # 注册 client
    logger.info('注册 client')
    http_client.register()

    # 开始轮询
    logger.info('开始循环获取命令')
    while True:
        # 获取命令
        command_dto = http_client.get_command()
        if command_dto.command is None:
            logger.info("命令为空")
            time.sleep(10)
            continue
        # 执行命令
        logger.info('命令是 ' + command_dto.command)
        stdout, stderr, duration = ExecutorService.run_command(command_dto.command)
        logger.info('命令执行完毕')
        # 上报结果
        http_client.report_command_result(stdout, stderr, duration, command_dto.deploy_execution_id)
        time.sleep(10)
