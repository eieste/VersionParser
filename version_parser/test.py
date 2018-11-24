from version_parser.version import Version

import unittest


class TestVersion(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(Version("v1.2.3").get_number(), 1002003)
        self.assertEqual(Version("vM1m2b3").get_number(), 1002003)
        self.assertEqual(Version("vM1m2p3").get_number(), 1002003)
        self.assertEqual(Version("v1_2_3").get_number(), 1002003)
        self.assertEqual(Version("1_2_3").get_number(), 1002003)
        self.assertEqual(Version("1.2.3").get_number(), 1002003)
        self.assertEqual(Version("V1.2.3").get_number(), 1002003)
        self.assertEqual(Version("v1.34.3").get_number(), 1034003)
        self.assertEqual(Version("v001.34.3").get_number(), 1034003)

    def test_compare(self):
        self.assertLess(Version("v1.2.3"), Version("v1.2.5"))
        self.assertGreater(Version("v1.2.3"), Version("v1.2.2"))
        self.assertGreaterEqual(Version("v1.2.3"), Version("v1.2.3"))
        self.assertGreaterEqual(Version("v1.2.4"), Version("v1.2.3"))
        self.assertEqual(Version("v1.2.3"), Version("v1.2.3"))


if __name__ == '__main__':
    unittest.main()
