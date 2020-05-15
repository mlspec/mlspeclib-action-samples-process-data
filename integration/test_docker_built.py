from pathlib import Path
import os
import sys
import unittest
import subprocess

sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / "bin"))

from utils import setupLogger  # noqa


class DockerBuildTester(unittest.TestCase):
    def setUp(self):
        (self.rootLogger, self._buffer) = setupLogger()

    def test_docker_build(self):
        container_name = os.environ.get(
            "INPUT_container_name", "mlspeclib-action-sample-process-data"
        )
        exec_statement = ["docker", "run", f"{container_name}:latest"]
        # p = subprocess.Popen(["docker"])
        # out, err = p.communicate()

        p = subprocess.Popen(
            exec_statement, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = p.communicate()
        self.rootLogger.debug(f"error = {str(err)}")
        self.assertTrue("ConfigurationException" in str(err))


if __name__ == "__main__":
    unittest.main()
