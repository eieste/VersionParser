# Version Parser

Der VersionParser kann Versionsnummer parsen und compare welche im format
Major-Version, Minor-Version und Build-Version aufgebaut sind.

Mögliche Eingabe Typen sind:
 * v1.2.3
 * V1.2.3
 * v_1_2_3
 * V_1_2_3
 * 1_2_3
 * v1_2_3
 * V1_2_3
 * VM1m2b3
 * VM1m2p3
 * vM1m2b3
 * vM1m2p3
 * 1.2.3


```python
from version_parser.version import Version

>> Version("v2.3.4")


>> Version("v2.3.4") < Version("v2.3.5")



>> v = Version("v2.3.4")
>> v.get_number()
2003004
>> v.get_major_version()
2
>> v.get_minor_version()
3
>> v.get_build_version()
4
>> v.get_type()
VersionType.Version
>> v.get_typed_version(Version.CLASSNAME)
VM2m3b4

```

## VersionTypes


### VersionType.FILENAME
```python
"v_{}_{}_{}".format(self._major_version, self._minor_version, self._build_version)
```

### VersionType.CLASSNAME
```python
"VM{}m{}b{}".format(self._major_version, self._minor_version, self._build_version)
```

### VersionType.VERSION
```python
"v{}.{}.{}".format(self._major_version, self._minor_version, self._build_version)
```

### VersionType.STRIPPED_VERSION
```python
"{}.{}.{}".format(self._major_version, self._minor_version, self._build_version)
```
