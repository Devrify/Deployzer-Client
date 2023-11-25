from dataclasses import dataclass
@dataclass
class RegistrationDto:
    ip:str
    uuid:str
    name:str