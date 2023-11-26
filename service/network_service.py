import requests
from dto.registration_dto import RegistrationDto
import dataclasses
import logging
import uuid
from common.deployzer_exception import DeployzerException
import json

class NetworkService:
    def __init__(self, url:str, token:str=None, name:str=None):
        self.url = url
        self.token = token
        self.name = name
        self._logger = logging.getLogger(__name__)

        # 注册 client
        try:
            self.register()
        except DeployzerException as e:
            raise DeployzerException('注册 client 失败') from e
        # 开始轮询

    def register(self):
        # 获取公网 ip
        try:
            ip = NetworkService.get_public_ip()
        except Exception as e:
            raise DeployzerException('获取公网 IP 失败') from e
        # 发送注册请求
        registration_dto = RegistrationDto(ip, str(uuid.uuid4()), self.name)
        try:
            response = self.post_json(dataclasses.asdict(registration_dto))
            NetworkService.response_check(response)
        except:
            raise

    def post_json(self, payload:dict) -> requests.Response:
        headers = {
            "Authorization":self.token
        }
        try:
            return requests.post(self.url, json=payload, headers=headers, timeout=5)
        except Exception as e:
            raise DeployzerException('Http 请求失败') from e

    @staticmethod
    def get_public_ip() -> str:
        return requests.get('https://ident.me', timeout=5).text.strip()

    @staticmethod
    def response_check(response:requests.Response):
        # http_code 检查
        if not response.ok:
            raise DeployzerException('服务器异常: ' + response.text)
        # http 响应检查
        response_decoded = response.content.decode('utf-8')
        response_json = json.loads(response_decoded)
        if response_json is None:
            raise DeployzerException('响应反序列化失败: ' + response_decoded)
        # 业务逻辑检查
        if response_json['code'] != 200:
            raise DeployzerException('响应 code 不为 200: ' + response_json)