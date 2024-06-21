# ======================================================================================================================

"""
Module to install/set up the SDK.
"""

# ======================================================================================================================

import os
import re
from setuptools import find_packages, setup


# ======================================================================================================================

def load_data(filename: str):
    """
    Loads content of a file in memory.
    """

    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()


def extract_version(filename: str):
    """
    Extracts the version from the specified Python file.
    """

    version_groups = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", load_data(filename),
        re.MULTILINE
    )

    if version_groups:
        return version_groups.group(1)

    raise RuntimeError(f"Unable to find version string in file '{filename}'.")


# ======================================================================================================================

setup(
    name='amberdata-derivatives',
    version=extract_version('amberdata_derivatives/version.py'),
    packages=find_packages(exclude='tests'),
    description='Python client for Amberdata API for derivatives analytics.',
    long_description=load_data('README.md'),
    long_description_content_type='text/markdown',
    author='Amberdata',
    license='Apache License',
    url='https://github.com/amberdata/amberdata-derivatives-sdk',
    install_requires=[
        'deprecation',
        'python-dotenv',
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
)

# ======================================================================================================================
