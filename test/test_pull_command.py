import subprocess
import unittest
import uuid
from pathlib import Path

from test import unit_test_utils

try:
    from test.unit_test_utils import AdbCommandTestCase, ANDROID_TEST_ROOT
except ModuleNotFoundError:  # pragma: no cover
    from unit_test_utils import AdbCommandTestCase, ANDROID_TEST_ROOT


class PullCommandTest(AdbCommandTestCase):
    local_dir_prefix = "better-adb-sync-pull"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._prepare_android_test_environment()

    def test_pull_command_copies_files_and_directories(self):
        destination = self.local_dir / "pull-target"
        destination.mkdir(parents=True, exist_ok=True)

        result = self.run_adb_sync_command("pull", ANDROID_TEST_ROOT, str(destination))
        self.assertEqual(
            result.returncode,
            0,
            msg=f"adbsync pull failed. stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
        )

        expected_root = destination / Path(ANDROID_TEST_ROOT).name
        self.assertTrue(expected_root.is_dir(), f"Expected pulled directory at {expected_root}")

        self.assertTrue((expected_root / "root.txt").is_file())
        self.assertEqual((expected_root / "root.txt").read_text(encoding="utf-8"), "root file")

        nested_dir = expected_root / "nested"
        self.assertTrue(nested_dir.is_dir())
        self.assertTrue((nested_dir / "empty").is_dir())
        self.assertTrue((nested_dir / "with_files" / "inner.txt").is_file())
        self.assertEqual((nested_dir / "with_files" / "inner.txt").read_text(encoding="utf-8"), "nested file")

        self.assertTrue((expected_root / ".hidden.txt").is_file())
        self.assertEqual((expected_root / ".hidden.txt").read_text(encoding="utf-8"), "hidden file")

        space_dir = expected_root / "folder with spaces"
        self.assertTrue(space_dir.is_dir())
        self.assertEqual((space_dir / "space file.txt").read_text(encoding="utf-8"), "space file")
        self.assertEqual((space_dir / "nbsp\xa0file.txt").read_text(encoding="utf-8"), "nbsp file")

        special_dir = space_dir / "nested (with) [brackets] & plus+sign"
        self.assertTrue(special_dir.is_dir())
        self.assertEqual((special_dir / "special!file#1+plus.txt").read_text(encoding="utf-8"), "special file")

        hash_dir = expected_root / "with#hash!and+plus"
        self.assertTrue(hash_dir.is_dir())
        self.assertEqual((hash_dir / "hash file.txt").read_text(encoding="utf-8"), "hash file")

        umlaut_dir = expected_root / "emoji-äöü"
        self.assertTrue(umlaut_dir.is_dir())
        self.assertEqual((umlaut_dir / "äöü.txt").read_text(encoding="utf-8"), "unicode file")

        smiley_dir = space_dir / "emoji-☺"
        self.assertTrue(smiley_dir.is_dir())
        self.assertEqual((smiley_dir / "smiley-☺.txt").read_text(encoding="utf-8"), "smiley file")

    @classmethod
    def _prepare_android_test_environment(cls):
        setup_script = unit_test_utils.REPO_ROOT / "test" / "android_test_setup.sh"
        if not setup_script.exists():
            raise FileNotFoundError(f"Missing Android test setup script at {setup_script}")

        remote_script = f"/data/local/tmp/better_adb_sync_setup_{uuid.uuid4().hex}.sh"
        subprocess.run(
            [cls.adb, "push", str(setup_script), remote_script],
            capture_output=True,
            text=True,
            check=True,
        )
        subprocess.run(
            [cls.adb, "shell", f"chmod 755 {remote_script}"],
            capture_output=True,
            text=True,
            check=True,
        )
        subprocess.run(
            [cls.adb, "shell", remote_script],
            capture_output=True,
            text=True,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
