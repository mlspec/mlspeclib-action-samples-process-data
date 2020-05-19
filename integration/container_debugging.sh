#!/bin/sh
pip install pipenv ipython
apt-get install vim git
git clone https://github.com/mlspec/mlspec-lib.git /mlspeclib

pip uninstall mlspeclib
pip install -e /mlspeclib
