#!/bin/bash

if [[ $(id -u) -ne 0 ]]; then
  echo "Please run as root"
  exit 1
fi

# Change directory to where this script is stored
cd "$(dirname $0)" || (echo "failed to change directory" && exit)

# Create a virtual environment to isolate our package dependencies locally
echo "Creating virtual env"
if python3 -m venv env; then
  source env/bin/activate # On Windows use `env\Scripts\activate`

  echo "Install requirements"
  pip install -r ./requirements.txt
  echo "Going to create database"
  sudo -u postgres createuser location_assignment_user
  sudo -u postgres createdb location_assignment
  sudo -u postgres psql -c "alter user location_assignment_user with encrypted password 'some_password';"
  sudo -u postgres psql -c "alter user location_assignment_user createdb;"
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE location_assignment TO location_assignment_user;"
else
  echo "Failed to create virtual env. Please check the log above"
fi
