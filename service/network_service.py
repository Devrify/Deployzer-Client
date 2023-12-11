import json

import requests
from pathlib import Path


from dto.get_command_response_dto import GetCommandResponseDto
from dto.registration_dto import RegistrationDto
from dto.report_command_result_dto import ReportCommandResultDto
import dataclasses
import logging
import uuid
from common.deployzer_exception import DeployzerException


class NetworkService:
    def __init__(self, url:str, token:str, name:str=None):
        self.ip = self.get_public_ip()
        self.url = url
        self.token = token
        self.name = name
        self.uuid = self.get_uuid()


        self._logger = logging.getLogger(__name__)

    '''
    注册 client， 会抛出 DeployzerException 异常
    '''
    def register(self):
        # 发送注册请求
        registration_dto = RegistrationDto(self.ip, self.uuid, self.name)
        try:
            self.post_authorized_json(self.url + '/deployzer/registration', dataclasses.asdict(registration_dto))
        except DeployzerException as e:
            raise DeployzerException('注册失败') from e

    '''
    获取命令， 会抛出 DeployzerException 异常
    '''
    def get_command(self) -> GetCommandResponseDto:
        # 创建查询
        query_dto = RegistrationDto(self.get_public_ip(), self.uuid, self.name)
        # 查询
        try:
            response_json = self.post_authorized_json(self.url + '/deployzer/get-command', dataclasses.asdict(query_dto))
        except DeployzerException as e:
            raise DeployzerException('获取命令失败') from e
        # 检查
        data = response_json['data']
        if 'command' not in data or 'deploy_execution_id' not in data:
            raise DeployzerException('命令或执行 id 为空')
        # 赋值
        return GetCommandResponseDto(data['command'], data['deploy_execution_id'])

    '''
    上报命令执行的结果， 会抛出 DeployzerException 异常
    '''
    def report_command_result(self, stdout:str, stderr, duration:float, deploy_execution_id:int):
        # 创建 dto
        report_command_result_dto \
            = ReportCommandResultDto(stdout, stderr, duration, deploy_execution_id)
        # 上报结果
        try:
            self.post_authorized_json(
                self.url + '/deployzer/report-command-result',
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
        try:
            return requests.get('https://ident.me', timeout=5).text.strip()
        except Exception as e:
            raise DeployzerException('获取公网 IP 失败') from e


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
            raise DeployzerException('响应反序列化失败: ' + response.text) from e
        # 业务逻辑检查
        if 'code' not in response_json:
            raise DeployzerException('没有响应 code' + str(response_json))
        if 'data' not in response_json:
            raise DeployzerException('没有 data' + str(response_json))
        if response_json['code'] != 200:
            raise DeployzerException('响应 code 不为 200: ' + str(response_json))
        return response_json


    '''
    从本地获取 uuid ， 没有则新建
    '''
    @staticmethod
    def get_uuid() -> str:
        path = './uuid.json'
        if Path(path).exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)['uuid']
            except Exception as e:
                raise DeployzerException('无法从文件反序列化 uuid') from e
        else:
            uuid_str = str(uuid.uuid4())
            data = {
                'uuid':uuid_str
            }
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                return uuid_str
            except Exception as e:
                raise DeployzerException('无法保存 uuid 到文件中') from e
