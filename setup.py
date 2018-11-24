import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="version_parser",
    version="0.0.1",
    author="Stefan Eiermann",
    author_email="pypip@ultraapp.de",
    description="This package can parse and compare semantic versioning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eieste/VersionParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)


