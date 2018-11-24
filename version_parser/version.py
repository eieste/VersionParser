import re
from enum import Enum


class VersionType(Enum):
    FILENAME = 1
    CLASSNAME = 2
    VERSION = 3
    STRIPPED_VERSION = 4
    NUMBER = 5
    CLASSNAME_PATCH = 6
    CLASSNAME_BUILD = 7


class Version:
    filename_pattern = re.compile(r"^[v|V]?[\_]?(?P<major>[0-9]+)\_(?P<minor>[0-9]+)\_(?P<build>[0-9]+)$")
    class_pattern = re.compile(r"^[v|V]?M(?P<major>[0-9]+)m(?P<minor>[0-9]+)(?P<type>[p|b])(?P<build>[0-9]+)$")
    version_pattern = re.compile(r"^[v|V](?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<build>[0-9]+)$")
    stripped_version_pattern = re.compile(r"^(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<build>[0-9]+)$")
    number_version_pattern = re.compile(r"^(\d{1,9})$")

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

        if type in [VersionType.CLASSNAME, VersionType.CLASSNAME_BUILD]:
            return "VM{}m{}b{}".format(self._major_version, self._minor_version, self._build_version)

        if type is VersionType.VERSION:
            return "v{}.{}.{}".format(self._major_version, self._minor_version, self._build_version)

        if type is VersionType.STRIPPED_VERSION:
            return "{}.{}.{}".format(self._major_version, self._minor_version, self._build_version)

        if type is VersionType.NUMBER:
            return self.get_number()

        if type is VersionType.CLASSNAME_PATCH:
            return "VM{}m{}p{}".format(self._major_version, self._minor_version, self._build_version)

    def _reverse(self, num):
        return str(num)[::-1]

    def _parse(self, any_version):
        result_dict = {
            "type": ValueError("Could not parse type"),
            "major": ValueError("Could not parse major"),
            "minor": ValueError("Could not parse minor"),
            "build": ValueError("Could not parse build")
        }

        str_version = str(any_version)
        result = False
        if self.filename_pattern.match(str_version):
            result = self.filename_pattern.match(str_version)
            result_dict["type"] = VersionType.FILENAME

        if self.class_pattern.match(str_version):
            result = self.class_pattern.match(str_version)
            result_dict["type"] = VersionType.CLASSNAME
            if result.group("type") == "p":
                result_dict["type"] = VersionType.CLASSNAME_PATCH
            elif result.group("type") == "b":
                result_dict["type"] = VersionType.CLASSNAME_BUILD

        elif self.version_pattern.match(str_version):
            result = self.version_pattern.match(str_version)
            result_dict["type"] = VersionType.VERSION

        elif self.stripped_version_pattern.match(str_version):
            result = self.stripped_version_pattern.match(str_version)
            result_dict["type"] = VersionType.STRIPPED_VERSION

        elif self.number_version_pattern.match(str_version):
            result = self.number_version_pattern.match(str_version)
            result_dict["type"] = VersionType.NUMBER

            reversed_nr = self._reverse(result.group(1))
            version_pices = [reversed_nr[i:i + 3] for i in range(0, len(reversed_nr), 3)]

            result_dict["build"] = int(self._reverse(version_pices[0]))

            if len(version_pices) > 1:
                result_dict["minor"] = int(self._reverse(version_pices[1]))
            else:
                result_dict["minor"] = 0

            if len(version_pices) > 2:
                result_dict["major"] = int(self._reverse(version_pices[2]))
            else:
                result_dict["major"] = 0

            return result_dict

        if not result:
            raise ValueError("Could not parse {}".format(str_version))

        result_dict["major"] = int(result.group("major"))
        result_dict["minor"] = int(result.group("minor"))
        result_dict["build"] = int(result.group("build"))

        return result_dict

    def get_type(self):
        return self._type

    def get_minor_version(self):
        return self._minor_version

    def get_major_version(self):
        return self._major_version

    def get_build_version(self):
        return self._build_version

    def get_patch_version(self):
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
