import unittest

from version_parser.version import Version, VersionType


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
        self.assertEqual(Version("1").get_number(), 1)
        self.assertEqual(Version("1001").get_number(), 1001)
        self.assertEqual(Version("1002003").get_number(), 1002003)
        self.assertEqual(Version("VM1m2p3").get_type(), VersionType.CLASSNAME_PATCH)
        self.assertEqual(Version("VM1m2b3").get_type(), VersionType.CLASSNAME_BUILD)

    def test_compare(self):
        self.assertLess(Version("v1.2.3"), Version("v1.2.5"))
        self.assertGreater(Version("v1.2.3"), Version("v1.2.2"))
        self.assertGreaterEqual(Version("v1.2.3"), Version("v1.2.3"))
        self.assertGreaterEqual(Version("v1.2.4"), Version("v1.2.3"))
        self.assertEqual(Version("v1.2.3"), Version("v1.2.3"))
        self.assertEqual(Version(1), Version("v0.0.1"))
        self.assertEqual(Version(2001), Version("v0.2.1"))
        self.assertEqual(Version(2001).compatible_version_with(Version("v0.2.1")), True)
        self.assertEqual(Version(2002).compatible_version_with(Version("v0.2.1")), True)
        self.assertEqual(Version(3002).compatible_version_with(Version("v0.2.1")), False)
        self.assertEqual(Version(3003002).compatible_version_with(Version("v3.2.1")), False)

    def test_output(self):
        self.assertEqual(Version(2001).get_typed_version(VersionType.VERSION), "v0.2.1")
        self.assertEqual(Version("v1.2.3").get_typed_version(VersionType.VERSION), "v1.2.3")
        self.assertEqual(Version("vM1m2p3").get_typed_version(VersionType.VERSION), "v1.2.3")
        self.assertEqual(Version(2001).get_typed_version(VersionType.FILENAME), "v_0_2_1")
        self.assertEqual(Version(2001).get_typed_version(VersionType.CLASSNAME), "VM0m2b1")
        self.assertEqual(Version("v_0_1_2").get_typed_version(VersionType.STRIPPED_VERSION), "0.1.2")
        self.assertEqual(Version("v_0_1_2").get_typed_version(VersionType.NUMBER), 1002)
        self.assertEqual(Version("v_0_1_2").get_typed_version(VersionType.CLASSNAME_PATCH), "VM0m1p2")
        self.assertEqual(Version("v_0_1_2").get_typed_version(VersionType.CLASSNAME_BUILD), "VM0m1b2")

    def test_fails(self):
        self.assertRaises(TypeError, Version)
        self.assertRaises(ValueError, Version, "asdf0.1.2")
        self.assertRaises(ValueError, Version, "VM1m2n3")
        self.assertRaises(ValueError, Version, "12345678901234")
        self.assertRaises(ValueError, Version, "p.y.p")
        self.assertRaises(ValueError, Version("v1.2.3").compatible_version_with, "asdf0.1.2")



if __name__ == '__main__':
    unittest.main()
