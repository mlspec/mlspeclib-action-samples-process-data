from pathlib import Path
import os
import sys
import unittest
import subprocess

sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / "bin"))
sys.path.append(str(Path.cwd().parent))

from utils.utils import setupLogger  # noqa


class DockerBuildTester(unittest.TestCase):
    def setUp(self):
        (self.rootLogger, self._buffer) = setupLogger().get_loggers()

    def test_docker_build(self):
        repo_name = os.environ.get(
            "INPUT_REPO_NAME", "mlspec"
        )
        container_name = os.environ.get(
            "INPUT_CONTAINER_NAME", "mlspeclib-action-samples-process-data"
        )
        exec_statement = ["docker", "run", f"{repo_name}/{container_name}:latest"]
        # p = subprocess.Popen(["docker"])
        # out, err = p.communicate()

        p = subprocess.Popen(
            exec_statement, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = p.communicate()
        self.rootLogger.debug(f"{str(err)}")
        self.assertTrue(p.returncode == 1)
        self.assertTrue("No value provided" in str(out))


if __name__ == "__main__":
    unittest.main()
