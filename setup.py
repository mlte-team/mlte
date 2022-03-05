"""
Package setup.
"""

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name="mlte",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "src/mlte/_version.py",
        "fallback_version": "0.1.0",
    },
    license="BSD-2-Clause",
    description="A toolkit for machine learning testing and evaluation.",
    author="Kyle Dotterrer",
    author_email="turingcompl33t@gmail.com",
    url="https://github.com/turingcompl33t/mlte",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/turingcompl33t/mlte/issues",
    },
    python_requires=">=3.7",
    setup_requires=[
        "setuptools_scm>=3.3.1",
    ],
)
