#! /bin/bash

# set environment variables 
export OAUTHLIB_INSECURE_TRANSPORT=1
export OAUTHLIB_INSECURE_TRANSPORT=1
export SECRET_KEY=udacity_secret
export FLASK_APP=app.py

# Do flask migration
flask db init
flask db migrate -m "Initial DB creation"
flask db upgrade

# Create some testing data
python add_data_to_db.py
