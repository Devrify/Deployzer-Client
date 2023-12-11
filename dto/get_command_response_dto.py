from dataclasses import dataclass


@dataclass
class GetCommandResponseDto:
    command:str
    deploy_execution_id: int