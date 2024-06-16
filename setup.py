# ======================================================================================================================

"""
Module to install/set up the SDK.
"""

# ======================================================================================================================

from setuptools import setup, find_packages

from amberdata_derivatives.version import __version__


# ======================================================================================================================

def load_data(filename: str):
    """
    Loads content of a file in memory.
    """

    with open(filename, encoding='utf-8') as f:
        return f.read()


# ======================================================================================================================

setup(
    name='amberdata-derivatives',
    version=__version__,
    packages=find_packages(),
    description='Python client for Amberdata API for derivatives analytics.',
    long_description=load_data('README.md'),
    long_description_content_type='text/markdown',
    author='Amberdata',
    url='https://github.com/amberdata/amberdata-derivatives-sdk',
    install_requires=[
        'deprecation',
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)

# ======================================================================================================================
