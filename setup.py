from setuptools import setup
version = '2.4.7'

setup(
    name='clearblade',
    packages=['clearblade'],
    install_requires=['requests', 'paho-mqtt>=1.3.0'],
    version=version,
    description='A Python SDK for interacting with the ClearBlade Platform.',
    url='https://github.com/ClearBlade/ClearBlade-Python-SDK',
    download_url='https://github.com/ClearBlade/ClearBlade-Python-SDK/archive/v' + version + '.tar.gz',
    keywords=['clearblade', 'iot', 'sdk'],
    maintainer='Aaron Allsbrook',
    maintainer_email='dev@clearblade.com'
)
