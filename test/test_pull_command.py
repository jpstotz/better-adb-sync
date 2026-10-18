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

    def test_pull_normal(self):
        destination = self.local_dir / "pull-target-normal"
        destination.mkdir(parents=True, exist_ok=True)

        source = f"{ANDROID_TEST_ROOT}/normal"
        result = self.run_adb_sync_command("pull", source, str(destination))
        self.assertEqual(result.returncode, 0,
                         msg=f"adbsync pull failed. stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
                         )

        expected_root = destination / Path(source).name
        self.assertTrue(expected_root.is_dir(), f"Expected pulled directory at {expected_root}")

        self.assertTrue((expected_root / "root.txt").is_file())
        self.assertEqual(read_text(expected_root / "root.txt"), "root file")

        nested_dir = expected_root / "nested"
        self.assertTrue(nested_dir.is_dir())
        self.assertTrue((nested_dir / "empty").is_dir())
        self.assertTrue((nested_dir / "with_files" / "inner.txt").is_file())
        self.assertEqual(read_text(nested_dir / "with_files" / "inner.txt"), "nested file")

        self.assertTrue((expected_root / ".hidden.txt").is_file())
        self.assertEqual(read_text(expected_root / ".hidden.txt"), "hidden file")

        space_dir = expected_root / "folder with spaces"
        self.assertTrue(space_dir.is_dir())
        self.assertEqual(read_text(space_dir / "space file.txt"), "space file")
        self.assertEqual(read_text(space_dir / "nbsp\xa0file.txt"), "nbsp file")

        special_dir = space_dir / "nested (with) [brackets] & plus+sign"
        self.assertTrue(special_dir.is_dir())
        self.assertEqual(read_text(special_dir / "special!file#1+plus.txt"), "special file")

        hash_dir = expected_root / "with#hash!and+plus"
        self.assertTrue(hash_dir.is_dir())
        self.assertEqual(read_text(hash_dir / "hash file.txt"), "hash file")

        umlaut_dir = expected_root / "emoji-äöü"
        self.assertTrue(umlaut_dir.is_dir())
        self.assertEqual(read_text(umlaut_dir / "äöü.txt"), "unicode file")

        smiley_dir = space_dir / "emoji-☺"
        self.assertTrue(smiley_dir.is_dir())
        self.assertEqual(read_text(smiley_dir / "smiley-☺.txt"), "smiley file")

    def test_pull_permission_denied(self):
        destination = self.local_dir / "pull-target-permission-denied"
        destination.mkdir(parents=True, exist_ok=True)

        source = f"{ANDROID_TEST_ROOT}/perm_denied"
        result = self.run_adb_sync_command("pull", source, str(destination))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Permission denied", f"{result.stdout}\n{result.stderr}")

    def test_pull_permission_denied_skip(self):
        destination = self.local_dir / "pull-target-permission-denied-skip"
        destination.mkdir(parents=True, exist_ok=True)

        source = f"{ANDROID_TEST_ROOT}/perm_denied"
        result = self.run_adb_sync_command("--skip-permission-denied", "pull", source, str(destination))
        self.assertEqual(result.returncode, 0,
                         msg=f"adbsync pull with --skip-permission-denied failed. stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}")

        expected_root = destination / Path(source).name
        self.assertTrue(expected_root.is_dir())
        self.assertTrue((expected_root / "a_accessible.txt").is_file())
        self.assertEqual(read_text(expected_root / "a_accessible.txt"), "root accessible A")
        self.assertTrue((expected_root / "b_blocked.txt").is_file())
        self.assertEqual(read_text(expected_root / "b_blocked.txt"), "")
        self.assertTrue((expected_root / "c_accessible.txt").is_file())
        self.assertEqual(read_text(expected_root / "c_accessible.txt"), "root accessible C")
        self.assertFalse((expected_root / "b_blocked_dir").exists())

        a_accessible_dir = expected_root / "a_accessible_dir"
        c_accessible_dir = expected_root / "c_accessible_dir"
        self.assertTrue(a_accessible_dir.is_dir())
        self.assertTrue((a_accessible_dir / "a_accessible.txt").is_file())
        self.assertEqual(read_text(a_accessible_dir / "a_accessible.txt"), "dir accessible A")
        self.assertTrue((a_accessible_dir / "b_blocked.txt").is_file())
        self.assertEqual(read_text(a_accessible_dir / "b_blocked.txt"), "")
        self.assertTrue(c_accessible_dir.is_dir())
        self.assertTrue((c_accessible_dir / "c_accessible.txt").is_file())
        self.assertEqual(read_text(c_accessible_dir / "c_accessible.txt"), "dir accessible C")

    @classmethod
    def _prepare_android_test_environment(cls):
        setup_script = unit_test_utils.REPO_ROOT / "test" / "android_test_setup.sh"
        if not setup_script.exists():
            raise FileNotFoundError(f"Missing Android test setup script at {setup_script}")

        remote_script = f"/data/local/tmp/better_adb_sync_setup_{uuid.uuid4().hex}.sh"
        subprocess.run([cls.adb, "push", str(setup_script), remote_script],
                       capture_output=True, text=True, check=True, )
        subprocess.run([cls.adb, "shell", f"chmod 755 {remote_script}"],
                       capture_output=True, text=True, check=True, )
        subprocess.run([cls.adb, "shell", remote_script],
                       capture_output=True, text=True, check=True, )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
