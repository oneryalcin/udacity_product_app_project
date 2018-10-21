#! /bin/bash

# Do flask migration
flask db init
flask db migrate -m " Initial DB creation"
flask db upgrade


