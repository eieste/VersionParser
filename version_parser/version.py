"""
Der version_parser kann Versionsnummer parsen und compare welche im format
Major-Version, Minor-Version und Build-Version aufgebaut sind.

Mögliche Eingabe Typen sind:
    v1.2.3
    V1.2.3
    v_1_2_3
    V_1_2_3
    1_2_3
    v1_2_3
    V1_2_3
    VM1m2b3
    VM1m2p3
    vM1m2b3
    vM1m2p3
    1.2.3

"""

import re
from enum import Enum


class VersionType(Enum):
    FILENAME = 1
    CLASSNAME = 2
    VERSION = 3
    STRIPPED_VERSION = 4


class Version:
    filename_pattern = re.compile(r"^[v|V]?[\_]?([0-9]+)\_([0-9]+)\_([0-9]+)$")
    class_pattern = re.compile(r"^[v|V]?M([0-9]+)m([0-9]+)[b|p]([0-9]+)$")
    version_pattern = re.compile(r"^[v|V]([0-9]+)\.([0-9]+)\.([0-9]+)$")
    stripped_version_pattern = re.compile(r"^([0-9]+)\.([0-9]+)\.([0-9]+)$")

    def __init__(self, raw_version):
        result = self._parse(raw_version)
        self._type = result["type"]
        self._major_version = result["major"]
        self._minor_version = result["minor"]
        self._build_version = result["build"]

        if isinstance(self._type, ValueError):
            raise self._type

    def __str__(self):
        return self.get_typed_version(self._type)

    def __lt__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_number() < other.get_number()

    def __le__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_number() <= other.get_number()

    def __eq__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_number() == other.get_number()

    def __ge__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_number() >= other.get_number()

    def __gt__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_number() > other.get_number()

    def __ne__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_number() != other.get_number()

    def get_number(self):
        filled_major = str(self._major_version).rjust(3, "0")
        filled_minor = str(self._minor_version).rjust(3, "0")
        filled_build = str(self._build_version).rjust(3, "0")
        return int("{}{}{}".format(filled_major, filled_minor, filled_build))

    def get_typed_version(self, type):
        if type is VersionType.FILENAME:
            return "v_{}_{}_{}".format(self._major_version, self._minor_version, self._build_version)

        if type is VersionType.CLASSNAME:
            return "VM{}m{}b{}".format(self._major_version, self._minor_version, self._build_version)

        if type is VersionType.VERSION:
            return "v{}.{}.{}".format(self._major_version, self._minor_version, self._build_version)

        if type is VersionType.STRIPPED_VERSION:
            return "{}.{}.{}".format(self._major_version, self._minor_version, self._build_version)

    def _parse(self, other_version):
        result_dict = {
            "type": ValueError("Could not parse type"),
            "major": ValueError("Could not parse major"),
            "minor": ValueError("Could not parse minor"),
            "build": ValueError("Could not parse build")
        }
        result = False
        if self.filename_pattern.match(other_version):
            result = self.filename_pattern.match(other_version)
            result_dict["type"] = VersionType.FILENAME

        if self.class_pattern.match(other_version):
            result = self.class_pattern.match(other_version)
            result_dict["type"] = VersionType.CLASSNAME

        if self.version_pattern.match(other_version):
            result = self.version_pattern.match(other_version)
            result_dict["type"] = VersionType.VERSION

        if self.stripped_version_pattern.match(other_version):
            result = self.stripped_version_pattern.match(other_version)
            result_dict["type"] = VersionType.STRIPPED_VERSION

        if not result:
            raise ValueError("Could not parse {}".format(other_version))

        result_dict["major"] = result.group(1)
        result_dict["minor"] = result.group(2)
        result_dict["build"] = result.group(3)

        return result_dict

    def get_type(self):
        return self._type

    def get_minor_version(self):
        return self._minor_version

    def get_major_version(self):
        return self._major_version

    def get_build_version(self):
        return self._build_version

    def compatible_version_with(self, other_version):
        """
        See same_version_as, but it doesnt check the build version
        Args:
            other_version: Any version String. Supportet VM999m999b999, v_999_999_99 v999.999.999
        Returns: (bool)

        """
        if isinstance(other_version, Version):
            result = {
                "major": other_version.get_major_version(),
                "minor": other_version.get_minor_version(),
                "build": other_version.get_build_version()
            }
        else:
            result = self._parse(other_version)

        if result["major"] == self._major_version and result["minor"] == self._minor_version:
            return True
        else:
            return False
