import requests

from dto.get_command_dto import GetCommandDto
from dto.registration_dto import RegistrationDto
from dto.report_command_result_dto import ReportCommandResultDto
import dataclasses
import logging
import uuid
from common.deployzer_exception import DeployzerException


class NetworkService:
    def __init__(self, url:str, token:str, name:str=None):
        try:
            self.ip = self.get_public_ip()
        except Exception as e:
            raise DeployzerException('获取公网 IP 失败') from e
        self.url = url
        self.token = token
        self.name = name
        self.uuid = str(uuid.uuid4())


        self._logger = logging.getLogger(__name__)

    '''
    注册 client， 会抛出 DeployzerException 异常
    '''
    def register(self):
        # 发送注册请求
        registration_dto = RegistrationDto(self.ip, self.uuid, self.name)
        try:
            self.post_authorized_json(self.url + '/register', dataclasses.asdict(registration_dto))
        except DeployzerException as e:
            raise DeployzerException('注册失败') from e

    '''
    获取命令， 会抛出 DeployzerException 异常
    '''
    def get_command(self) -> GetCommandDto:
        # 创建查询
        query_dto = RegistrationDto(self.get_public_ip(), self.uuid, self.name)
        # 查询
        try:
            response_json = self.post_authorized_json(self.url + '/get-command', dataclasses.asdict(query_dto))
        except DeployzerException as e:
            raise DeployzerException('获取命令失败') from e
        # 赋值
        return GetCommandDto(response_json['command'])

    '''
    上报命令执行的结果， 会抛出 DeployzerException 异常
    '''
    def report_command_result(self, stdout:str, stderr, duration:float):
        # 创建查询
        report_command_result_dto = ReportCommandResultDto(self.ip, self.uuid, self.name, stdout, stderr, duration)
        # 上报结果
        try:
            self.post_authorized_json(
                self.url + '/report-command-result',
                dataclasses.asdict(report_command_result_dto)
            )
        except DeployzerException as e:
            raise DeployzerException('获取命令失败') from e

    '''
    发送带认证头的请求， 会抛出 DeployzerException 异常
    '''
    def post_authorized_json(self, url:str, payload:dict) -> dict:
        headers = {
            "Authorization":self.token
        }
        # 发送请求
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
        except Exception as e:
            raise DeployzerException('发送 Http 请求失败') from e
        # 响应检查
        try:
            return self.response_check(response)
        except:
            raise

    '''
    从远端获取 ip 地址， 会抛出 Exception 异常
    '''
    @staticmethod
    def get_public_ip() -> str:
        return requests.get('https://ident.me', timeout=5).text.strip()


    '''
    检查服务返回的 response， 会抛出 DeployzerException 异常
    '''
    @staticmethod
    def response_check(response:requests.Response) -> dict:
        # http_code 检查
        if not response.ok:
            raise DeployzerException('服务器异常: ' + response.text)
        # http 响应检查
        try:
            response_json = response.json()
        except Exception as e:
            raise DeployzerException('响应反序列化失败: ' + str(response)) from e
        # 业务逻辑检查
        if response_json['code'] != 200:
            raise DeployzerException('响应 code 不为 200: ' + response_json)
        return response_json
