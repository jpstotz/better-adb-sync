import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ANDROID_TEST_ROOT = "/data/local/tmp/better_adb_sync_tests"


class AdbCommandTestCase(unittest.TestCase):
    local_dir_prefix = "better-adb-sync"

    @classmethod
    def setUpClass(cls):
        adb = shutil.which("adb")
        if adb is None:
            raise unittest.SkipTest("adb is not available on PATH")

        result = subprocess.run(
            [adb, "devices"],
            capture_output=True,
            text=True,
            check=False,
        )
        if "device" not in result.stdout.lower():
            raise unittest.SkipTest("No Android device connected")

        cls.adb = adb
        cls.local_dir = Path(tempfile.mkdtemp(prefix=f"{cls.local_dir_prefix}-"))

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "local_dir", None) and cls.local_dir.exists():
            shutil.rmtree(cls.local_dir, ignore_errors=True)

        subprocess.run(
            [cls.adb, "shell", "rm -rf /data/local/tmp/*"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _adb_shell(self, command: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.adb, "shell", command],
            capture_output=True,
            text=True,
            check=True,
        )

    def run_adb_sync_command(self, *args):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "BetterADBSync", *args],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
