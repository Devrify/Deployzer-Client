import subprocess
import time


class ExecutorService:

    @staticmethod
    def run_command(command:str) -> (str, str, float):
        if command is None:
            raise Exception('命令为空')
        start_time = time.time_ns()
        result = subprocess.run(
            [command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True
        )
        end_time = '{:.2f}'.format((time.time_ns() - start_time) / 1000 / 1000)
        return result.stdout, result.stderr, end_time