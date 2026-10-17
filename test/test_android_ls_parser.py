import unittest

from BetterADBSync.FileSystems.Android import AndroidFileSystem


class AndroidLsParserTest(unittest.TestCase):
    def setUp(self):
        self.fs = AndroidFileSystem.__new__(AndroidFileSystem)

    def test_selinux_protected_entries_are_permission_denied(self):
        cases = [
            "-?????????    ? ?      ?             ?                ? init.environ.rc",
            "d?????????    ? ?      ?             ?                ? data_mirror",
            "l?????????    ? ?      ?             ?                ? cache -> ?",
        ]

        for line in cases:
            with self.subTest(line=line):
                with self.assertRaises(PermissionError) as error:
                    self.fs.ls_to_stat(line)
                self.assertIn(error.exception.filename, line)

    def test_valid_ls_line_still_parses(self):
        filename, stat_result = self.fs.ls_to_stat(
            "-rw-r--r-- 1 root root 123 2025-04-01 12:34 example.txt"
        )
        self.assertEqual(filename, "example.txt")
        self.assertEqual(stat_result.st_size, 123)


if __name__ == "__main__":
    unittest.main()
