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
    version_pattern = re.compile(r"^[vV](?P<major>[0-9]+)(?:\.(?P<minor>[0-9]+)(?:\.(?P<build>[0-9]+))?)?$")
    stripped_version_pattern = re.compile(r"^(?P<major>[0-9]+)(?:\.(?P<minor>[0-9]+)(?:\.(?P<build>[0-9]+))?)?$")

    # Removed number_version_pattern from parsing logic. Instead we use a dedicated constructor.
    # number_version_pattern = re.compile(r"^(\d{1,9})$")

    def __init__(self, raw_version: str):
        if isinstance(raw_version, int):
            raise ValueError("To create a version from a number, use Version.from_number(<int>)")
        result = self._parse(raw_version)
        self._type = result["type"]
        self._major_version = result["major"]
        self._minor_version = result["minor"]
        self._build_version = result["build"]

        if isinstance(self._type, ValueError):
            raise self._type

    @classmethod
    def from_number(cls, number):
        """
        Create a Version object from an integer, using the legacy logic.
        
        Example:
            2001 -> v0.2.1
        """
        str_num = str(number)
        if not str_num.isdigit():
            raise ValueError("from_number expects a positive integer")

        reversed_nr = str_num[::-1]
        # Split reversed number into chunks of 3
        version_pieces = [reversed_nr[i:i + 3] for i in range(0, len(reversed_nr), 3)]

        # Extract build
        build = int(version_pieces[0][::-1])
        # Extract minor if available
        minor = int(version_pieces[1][::-1]) if len(version_pieces) > 1 else 0
        # Extract major if available
        major = int(version_pieces[2][::-1]) if len(version_pieces) > 2 else 0

        v = cls(f"v{major}.{minor}.{build}")
        # Set type as NUMBER to preserve old behavior if needed.
        v._type = VersionType.NUMBER
        return v
    
    def __repr__(self) -> str:
        return f"Version[{self._major_version}.{self._minor_version}.{self._build_version}]"

    def __str__(self):
        return self.get_typed_version(self._type)

    def __lt__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_tuple() < other.get_tuple()

    def __le__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_tuple() <= other.get_tuple()

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.get_tuple() == other.get_tuple()

    def __ge__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_tuple() >= other.get_tuple()

    def __gt__(self, other):
        assert isinstance(other, self.__class__)
        return self.get_tuple() > other.get_tuple()

    def __ne__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.get_tuple() != other.get_tuple()

    def get_tuple(self):
        """Returns the version as a tuple (major, minor, build) for easy comparison."""
        return (self._major_version, self._minor_version, self._build_version)

    def get_number(self):
        # Legacy Number support
        filled_major = str(self._major_version).rjust(3, "0")
        filled_minor = str(self._minor_version).rjust(3, "0")
        filled_build = str(self._build_version).rjust(3, "0")
        return int(f"{filled_major}{filled_minor}{filled_build}")

    def get_typed_version(self, type):
        if type is VersionType.FILENAME:
            return f"v_{self._major_version}_{self._minor_version}_{self._build_version}"

        if type in [VersionType.CLASSNAME, VersionType.CLASSNAME_BUILD]:
            return f"VM{self._major_version}m{self._minor_version}b{self._build_version}"

        if type is VersionType.VERSION:
            return f"v{self._major_version}.{self._minor_version}.{self._build_version}"

        if type is VersionType.STRIPPED_VERSION:
            return f"{self._major_version}.{self._minor_version}.{self._build_version}"

        if type is VersionType.NUMBER:
            # _legacy_number_format: If needed, return the number as before:
            return self.get_number() 

        if type is VersionType.CLASSNAME_PATCH:
            return f"VM{self._major_version}m{self._minor_version}p{self._build_version}"

        #// If we can't determine type, fall back to a standard version string
        return f"v{self._major_version}.{self._minor_version}.{self._build_version}"

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

        elif self.class_pattern.match(str_version):
            result = self.class_pattern.match(str_version)
            # By default it's a CLASSNAME:
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

        if not result:
            raise ValueError(f"Could not parse {str_version}")

        result_dict["major"] = int(result.group("major")) if result.group("major") else 0
        result_dict["minor"] = int(result.group("minor")) if result.group("minor") else 0
        result_dict["build"] = int(result.group("build")) if result.group("build") else 0

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
        Checks if major and minor match between self and other_version.
        """
        if isinstance(other_version, Version):
            result_major = other_version.get_major_version()
            result_minor = other_version.get_minor_version()
        else:
            # parse as a version string
            result = self._parse(other_version)
            result_major = result["major"]
            result_minor = result["minor"]

        return (result_major == self._major_version and result_minor == self._minor_version)