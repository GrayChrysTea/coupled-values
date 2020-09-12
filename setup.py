from setuptools import find_packages, setup, Extension
import unittest

def test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="tests_*.py")
    return suite

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="coupled-values",
    version="0.1.0rc2",
    author="GrayChrysTea",
    description="A more dynamic version of Python dictionaries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrayChrysTea/coupled-values",
    packages=find_packages(),
    test_suite="setup.test_suite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
