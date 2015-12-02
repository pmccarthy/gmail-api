#!/usr/bin/env bash

OS=$(uname -s)

if [[ $(which easy_install) ]]; then
  echo "Python setuptools and easy_install already configured. Skipping"
else
  echo "Installing python setuptools and easy_install package"
  if [[ $OS == 'Darwin' ]]; then
    echo "Detected Operating System: Darwin"
    curl https://bootstrap.pypa.io/ez_setup.py -o - | python
  elif [[ $OS == 'Linux' ]]; then
    echo "Detected Operating System: Linux"
    wget https://bootstrap.pypa.io/ez_setup.py -O - | python
  else
    echo "Unsupported OS $OS. Supported Operating Systems: Darwin Linux"
  fi
fi

packages="httplib2 datetime google-api-python-client termcolor"

echo "Installing required python packages via easy_install"
for package in $packages; do
  sudo easy_install --upgrade $package;
done