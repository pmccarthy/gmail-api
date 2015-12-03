## Gmail API Wrapper Script
The purpose of this script is to retrieve various statistics from Gmail using the Gmail API: https://developers.google.com/gmail/api/?hl=en


## Supported Operating Systems
* Darwin
* Linux
  
## Prerequisites
Before the script can be run, there is a requirement for a client_secret.json file to be present in the root of this repository. This file can be generated by following the tutorial from the Google Gmail API Docs: https://developers.google.com/gmail/api/quickstart/python

## Setup
To install all required dependencies please run the setup.sh script

`bash setup.sh`

This script installs python setuptools (if not already present) and will use easy_install to install all required python packages.

## Usage
For now the only statistics being retrieved are the number of emails received from a specific user on a particular day.

Sample command

`python gmail-query.py -s <user> -y 2015 -m 12 -d 01`
