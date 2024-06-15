from setuptools import setup, find_packages

import sys
sys.path[0:0] = ['amberdata_derivatives']

from version import __version__

setup(
    name='amberdata-derivatives',
    version=__version__,
    packages=find_packages(),
    description='Python client for Amberdata API for derivatives analytics.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Amberdata',
    url='https://github.com/amberdata/amberdata-derivatives-sdk',
    install_requires=[
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
