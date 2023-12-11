from dataclasses import dataclass

from dto.registration_dto import RegistrationDto


@dataclass
class ReportCommandResultDto:
    stdout:str
    stderr:str
    duration:float
    deploy_execution_id:int