import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = REPO_ROOT / "test"
sys.path.insert(0, str(REPO_ROOT))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(TEST_DIR), pattern="test_*.py", top_level_dir=str(REPO_ROOT))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
