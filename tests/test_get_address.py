import ipaddress
import unittest

from utils.get_address import DEFAULT_UCAS_NETWORKS, parse_linux_output


class ParseLinuxOutputTest(unittest.TestCase):
    def test_matches_current_ucas_private_network(self):
        stdout = """\
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
    inet 127.0.0.1/8 scope host lo
2: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet 10.211.1.67/21 brd 10.211.7.255 scope global eth1
"""
        networks = [ipaddress.ip_network(n) for n in DEFAULT_UCAS_NETWORKS]

        self.assertEqual(
            parse_linux_output(stdout, networks),
            {"eth1": "10.211.1.67"},
        )

    def test_ignores_unrelated_networks(self):
        stdout = """\
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
    inet 127.0.0.1/8 scope host lo
2: br-lan: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet 10.3.1.10/16 brd 10.3.255.255 scope global br-lan
"""
        networks = [ipaddress.ip_network(n) for n in DEFAULT_UCAS_NETWORKS]

        self.assertEqual(parse_linux_output(stdout, networks), {})


if __name__ == "__main__":
    unittest.main()
