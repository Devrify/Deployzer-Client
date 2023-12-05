import subprocess
import time


class ExecutorService:

    @staticmethod
    def run_command(command:str) -> (str, str, float):
        if command is None:
            raise Exception('命令为空')
        start_time = time.time()
        result = subprocess.run(
            [command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True
        )
        end_time = '{:.2f}'.format(time.time() - start_time)
        return result.stdout, result.stderr, end_time