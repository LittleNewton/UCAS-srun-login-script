#!/usr/bin/env python

from pathlib import Path
import stat
import sys

from BitSrunLogin.LoginManager import LoginManager
from utils.get_address import find_interface_in_network


KEY_FILE = Path(__file__).resolve().parent / "config" / "key"


def load_password(key_file=KEY_FILE):
    mode = stat.S_IMODE(key_file.stat().st_mode)
    if mode != 0o600:
        raise PermissionError(f"{key_file} must have mode 600")

    password = key_file.read_text(encoding="utf-8").rstrip("\r\n")
    if not password:
        raise ValueError(f"{key_file} is empty")
    return password


def main():
    try:
        ip_info = find_interface_in_network()
        if not ip_info:
            raise RuntimeError("no UCAS network interface found")

        password = load_password()
        lm = LoginManager()
        for interface, ip_address in ip_info.items():
            print(f"Logging in {interface} ({ip_address})")
            lm.login(
                username="liupeng19@mails.ucas.edu.cn",
                password=password,
                ip=ip_address,
            )
            return 0
    except Exception as e:
        print(f"UCAS login failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
