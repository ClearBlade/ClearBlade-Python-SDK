from setuptools import setup

setup(
    name='clearblade',
    packages=['clearblade'],
    install_requires=['requests', 'paho-mqtt>=1.3.0'],
    version='2.2.3',
    description='A Python SDK for interacting with the ClearBlade Platform.',
    url='https://github.com/ClearBlade/ClearBlade-Python-SDK',
    download_url='https://github.com/ClearBlade/ClearBlade-Python-SDK/archive/v2.2.3.tar.gz',
    keywords=['clearblade', 'iot', 'sdk'],
    maintainer='Aaron Allsbrook',
    maintainer_email='dev@clearblade.com'
)
