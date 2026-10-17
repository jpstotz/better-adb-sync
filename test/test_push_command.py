import unittest

try:
    from test.unit_test_utils import AdbCommandTestCase, ANDROID_TEST_ROOT
except ModuleNotFoundError:  # pragma: no cover
    from unit_test_utils import AdbCommandTestCase, ANDROID_TEST_ROOT


class PushCommandTest(AdbCommandTestCase):
    local_dir_prefix = "better-adb-sync-push"

    def test_push_command_copies_files_and_directories(self):
        self._adb_shell(f"rm -rf {ANDROID_TEST_ROOT}")

        source_dir = self.local_dir / "push-source"
        nested_dir = source_dir / "nested" / "with_files"
        nested_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / "nested" / "empty").mkdir(parents=True, exist_ok=True)
        (source_dir / "root.txt").write_text("root file", encoding="utf-8")
        (nested_dir / "inner.txt").write_text("nested file", encoding="utf-8")
        (source_dir / ".hidden.txt").write_text("hidden file", encoding="utf-8")

        result = self.run_adb_sync_command("push", str(source_dir), ANDROID_TEST_ROOT)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"adbsync push failed. stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
        )

        self.assertEqual(self._adb_shell(f"cat {ANDROID_TEST_ROOT}/root.txt").stdout.strip(), "root file")
        self.assertTrue(self._adb_shell(f"test -d {ANDROID_TEST_ROOT}/nested").returncode == 0)
        self.assertTrue(self._adb_shell(f"test -d {ANDROID_TEST_ROOT}/nested/empty").returncode == 0)
        self.assertEqual(self._adb_shell(f"cat {ANDROID_TEST_ROOT}/nested/with_files/inner.txt").stdout.strip(), "nested file")
        self.assertEqual(self._adb_shell(f"cat {ANDROID_TEST_ROOT}/.hidden.txt").stdout.strip(), "hidden file")


if __name__ == "__main__":
    unittest.main()
