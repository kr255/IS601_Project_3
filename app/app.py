import os
from typing import List, Dict
import mysql.connector
import simplejson
from flask import Flask, Response
from dotenv import load_dotenv

# load_dotenv()
# username = os.getenv('user')
# password = os.getenv('DB_PASSWORD')
# host = os.getenv('host')
# port = os.getenv('port')
# database = os.getenv('database')

app = Flask(__name__)

def cities_import() -> List[Dict]:

    config = {

        'user': 'root',
        'password' : 'root',
        'host':'db',
        'port': '3306',
        'database': 'citiesData'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result


@app.route('/')
def index() -> str:
    js = simplejson.dumps(cities_import())
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')