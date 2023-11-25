import requests
from dto.registration_dto import RegistrationDto
import dataclasses
import logging

class HttpClient:
    def __init__(self, url:str, token:str=None):
        self.url = url
        self.token = token
        self._logger = logging.getLogger(__name__)

    def register(self):
        pass