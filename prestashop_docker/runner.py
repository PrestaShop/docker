import sys
from subprocess import Popen, PIPE


class Runner:
    def run(self, cmd, stdout=True):
        if stdout:
            params = {
                'stdout': sys.stdout,
                'stderr': sys.stderr,
            }
        else:
            params = {
                'stdout': PIPE,
                'stderr': PIPE,
            }

        proc = Popen(
            cmd,
            **params
        )

        if not stdout:
            stdout, stderr = proc.communicate()
            return [stdout, stderr]
