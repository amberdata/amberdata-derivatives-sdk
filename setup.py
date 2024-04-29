from setuptools import setup, find_packages

setup(
    name='amberdata-derivatives',
    version='1.0.0',
    packages=find_packages(),
    description='Python client for Amberdata API for derivatives analytics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Amberdata',
    author_email='fabio.bassani@amberdata.io',
    #url='https://github.com/tuo_username/amberdata-derivatives',
    url='https://github.com/gravity5ucks/amberdata-derivatives-py',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)