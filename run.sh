#!/bin/sh
echo 'Begin to run backend'
pip3 install -r api/requirements.txt
export POSTGRES_PASSWORD="your_postgres_password"
python3 api/save_data_to_table.py
python3 api/app.py