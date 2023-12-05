from dataclasses import dataclass

from dto.registration_dto import RegistrationDto


@dataclass
class ReportCommandResultDto(RegistrationDto):
    stdout:str
    stderr:str
    duration:float