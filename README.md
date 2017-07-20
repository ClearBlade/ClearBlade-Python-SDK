Python-SDK
==========

A python SDK for interacting with the ClearBlade Platform.

Currently under a rewrite, not all features have been implemented yet and no documentation or sample code exists yet.

## Installation

### To install for regular use:
1. Clone or download this repo on to your machine.
2. Run `python setup.py install`.

### To install for development (of the sdk):
1. Clone or download this repo on to your machine.
2. Run `python setup.py develop`. This creates a folder called ClearBlade.egg-info in your current directory. You will now be allowed to import the sdk _in the current directory_, and any changes you make to the sdk code will automatically be updated in the egg.

## Usage
The intended entry point for the sdk is the ClearBladeCore file. The beginning of your python file should include a line like the following:
`from clearblade.ClearBladeCore import System, Query, Developer`
System, Query, and Developer are the only three classes you should ever need to import directly into your project.

## Documentation
Documentation is under construction.