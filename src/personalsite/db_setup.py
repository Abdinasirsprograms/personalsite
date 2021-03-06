import os
import json
from django.core.exceptions import ImproperlyConfigured
import mysql.connector

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

mydb = mysql.connector.connect(
  user="root",
  password=""
)

mycursor = mydb.cursor()

mycursor.execute('CREATE DATABASE personalsite',)

secret_pass = get_secret('DB_PASSWORD')

mycursor.execute(f'CREATE USER \'abdi\'@\'localhost\' IDENTIFIED BY \'{secret_pass}\'; \
                GRANT ALL ON *.* TO \'abdi\'@\'localhost\' WITH GRANT OPTION;',)

mycursor.close()
