import unittest
from pathlib import Path

try:
    from test.unit_test_utils import AdbCommandTestCase, ANDROID_TEST_ROOT
except ModuleNotFoundError:  # pragma: no cover
    from unit_test_utils import AdbCommandTestCase, ANDROID_TEST_ROOT


class PullCommandTest(AdbCommandTestCase):
    local_dir_prefix = "better-adb-sync-pull"

    def test_pull_command_copies_files_and_directories(self):
        self._adb_shell(f"rm -rf /data/local/tmp/*")
        self._adb_shell(f"mkdir -p {ANDROID_TEST_ROOT}/nested/empty {ANDROID_TEST_ROOT}/nested/with_files")
        self._adb_shell(f"printf '%s' 'root file' > {ANDROID_TEST_ROOT}/root.txt")
        self._adb_shell(f"printf '%s' 'nested file' > {ANDROID_TEST_ROOT}/nested/with_files/inner.txt")
        self._adb_shell(f"printf '%s' 'hidden file' > {ANDROID_TEST_ROOT}/.hidden.txt")

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


if __name__ == "__main__":
    unittest.main()
