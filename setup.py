import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="version_parser",
    version="1.0.1",
    author="Stefan Eiermann",
    author_email="python-org@ultraapp.de",
    description="This package can parse and compare semantic versioning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eieste/VersionParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: JavaScript",
        "Development Status :: 5 - Production/Stable"
    ],
)


