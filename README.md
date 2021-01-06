# Version Parser


## JavaScript Version

[https://www.npmjs.com/package/version-parser](https://www.npmjs.com/package/version-parser)

[![npm version](https://badge.fury.io/js/version-parser.svg)](https://badge.fury.io/js/version-parser)

## Python Version

[![Build Status](https://travis-ci.org/eieste/VersionParser.svg?branch=master)](https://travis-ci.org/eieste/VersionParser)
[![PyPI version](https://badge.fury.io/py/version-parser.svg)](https://badge.fury.io/py/version-parser)

The version parser is able to parse versions and figure out which of them are build in
one of the following three formats: Major-Version, Minor-Version and Build-Version.

Possible input types are:

| Version  | Typ               |
|----------|-------------------|
| v1.2.3   | Version           |
| V1.2.3   | Version           |
| v_1_2_3  | FILENAME          |
| v1_2_3   | FILENAME          |
| V_1_2_3  | FILENAME          |
| V1_2_3   | FILENAME          |
| 1_2_3    | FILENAME          |
| VM1m2b3  | CLASSNAME_BUILD   |
| VM1m2p3  | CLASSNAME_PATCH   |
| vM1m2b3  | CLASSNAME_BUILD   |
| vM1m2p3  | CLASSNAME_PATCH   |
| 1.2.3    | STRIPPED_VERSION  |
| 2312     | NUMBER            |


## Install
```python
pip install version-parser
```

## Usage

Create object with the version as a String as initial parameter.

```python
from version_parser import Version


v1 = Version("v2.3.4")
```


To compare two version objects/numbers, simply put the versions as Strings into 
seperate objects and compare them using the logical operators.
```python
from version_parser.version import Version


v1 = Version("v2.3.4")
v2 = Version("v2.3.2")

print(v1 < v2)
>> False


print(v1 > v2)
>> True


print(v1 == v2)
>> False

```


The last digets behind the last dot should be the Patch or Build Version Number.
Differences in this area should be compatible to each other.
```python
from version_parser.version import Version


v1 = Version("v2.3.4")
v2 = Version("v2.3.5")


print(v1 == v2)
>> False


print(v1.compatible_version_with(v2))
>> True

```

You can also get only the Major, Minor or Build Version by using:

````python
from version_parser import Version
v = Version("v2.3.4")

v.get_major_version()
2
v.get_minor_version()
3
v.get_build_version()
4
````

It's possible to convert the version format, too:

````python
from version_parser import Version, VersionType
v = Version("v2.3.4")       # VersionType = Version
print(v.get_type())
>> VersionType.Version

print(v.get_typed_version(VersionType.FILENAME))
>> v_2_3_4
````

Any version can be represented by an Integer.
> The sections of major, minor, build/patched version should have a maximum of three digets.

````python
from version_parser import Version
v = Version("v2.3.4")
print(v.get_number())
>> 2003004
````


## VersionTypes

### VersionType.FILENAME
```python
"v_<MAJOR>_<MINOR>_<BUILD/PATCH>"
```

### VersionType.CLASSNAME
```python
"VM<MAJOR>m<MINOR>b<BUILD/PATCH>"
```

### VersionType.VERSION
```python
"v<MAJOR>.<MINOR>.<BUILD/PATCH>"
```

### VersionType.STRIPPED_VERSION
```python
"<MAJOR>.<MINOR>.<BUILD/PATCH>"
```

### VersionType.NUMBER
> each section is filled zeros up to three digets
```python
"<MAJOR><MINOR><BUILD/PATCH>"
```

### VersionType.CLASSNAME_BUILD
> same like CLASSNAME_BUILD 


### VersionType.CLASSNAME_PATCH
```python
"VM<MAJOR>m<MINOR>p<BUILD/PATCH>"
                  ^
                PATCH 
```

