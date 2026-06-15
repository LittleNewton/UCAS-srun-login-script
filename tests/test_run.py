import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.modules.setdefault("requests", MagicMock())
import run


class RunTest(unittest.TestCase):
    def test_loads_password_from_private_key_file(self):
        with tempfile.TemporaryDirectory() as directory:
            key_file = Path(directory) / "key"
            key_file.write_text("secret\n", encoding="utf-8")
            key_file.chmod(0o600)

            self.assertEqual(run.load_password(key_file), "secret")

    def test_rejects_permissive_key_file(self):
        with tempfile.TemporaryDirectory() as directory:
            key_file = Path(directory) / "key"
            key_file.write_text("secret\n", encoding="utf-8")
            key_file.chmod(0o644)

            with self.assertRaises(PermissionError):
                run.load_password(key_file)

    @patch("run.find_interface_in_network", return_value={})
    def test_returns_failure_when_no_ucas_interface_is_found(self, _find):
        self.assertEqual(run.main(), 1)

    @patch("run.load_password", return_value="secret")
    @patch("run.LoginManager")
    @patch(
        "run.find_interface_in_network",
        return_value={"eth1": "10.211.1.67"},
    )
    def test_logs_in_matching_interface(
        self,
        _find,
        login_manager,
        _load_password,
    ):
        self.assertEqual(run.main(), 0)
        login_manager.return_value.login.assert_called_once_with(
            username="liupeng19@mails.ucas.edu.cn",
            password="secret",
            ip="10.211.1.67",
        )


if __name__ == "__main__":
    unittest.main()
