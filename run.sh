#!/bin/sh
echo 'Begin to run backend'
pip3 install -r api/requirements.txt
python3 api/save_data_to_table.py
# on mac it's export, if you are using windows, please use 'set POSTGRES_PASSWORD="your_postgres_password"' instead
export POSTGRES_PASSWORD="your_postgres_password"
python3 api/app.py