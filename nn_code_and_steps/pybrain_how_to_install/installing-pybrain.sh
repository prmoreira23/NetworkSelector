#!/bin/bash

# This script set up pybrain
# Install PyBrain and its dependencies
# git, python, scipy, matplotlib

sudo apt-get install git python python-scipy python-matplotlib -y
sudo python ez_setup.py 
git clone git://github.com/pybrain/pybrain.git pybrain
cd pybrain;sudo python setup.py install;cd ..;rm -R pybrain