from setuptools import setup, find_packages
import unittest

def test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="tests_*.py")
    return suite

with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

setup(
    name="coupled-values",
    version="1.0.0",
    author="GrayChrysTea",
    author_email="gray.chrysanthemum@gmail.com",

    packages=[
        "coupledpairs",
        "coupledvalues",
        "coupledvalues.coupledvalues",
        "coupledvalues.constants",
        "coupledvalues.errors"
    ],

    install_requires=[],

    description="A set of coupled values where either side can be the key.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrayChrysTea/coupled-values",

    test_suite="setup.test_suite",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
