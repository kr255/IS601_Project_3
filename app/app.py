import os
from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = os.environ['host']
app.config['MYSQL_DATABASE_USER'] = os.environ['user']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('pass')
app.config['MYSQL_DATABASE_PORT'] = int(os.environ['port'])
app.config['MYSQL_DATABASE_DB'] = os.environ['database']

# app.config['MYSQL_DATABASE_HOST'] = 'db'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_PORT'] = 3306
# app.config['MYSQL_DATABASE_DB'] = 'citiesData'
mysql.init_app(app)

# print(os.environ.get('pass'))
# print(os.environ.get('database'))
# print(os.environ.get('host'))

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Addresses Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE Address_id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE Address_id=%s', int(city_id))
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 int(request.form.get('fldCapitalStatus')), city_id)
    sql_update_query = """UPDATE addresses t SET t.First_Name = %s, t.City = %s, t.State = %s, t.Street =
    %s, t.Last_Name = %s, t.Postal_Code = %s WHERE t.Address_id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/addresses/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Address Form')


@app.route('/addresses/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO addresses (First_Name,City,State,Street,Last_Name,Postal_Code,Address_id) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM addresses WHERE Address_id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE Address_id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldName'], content['fldLat'], content['fldLong'],
                 content['fldCountry'], content['fldAbbreviation'],
                 content['fldCapitalStatus'], content['fldPopulation'],city_id)
    sql_update_query = """UPDATE addresses t SET t.First_Name = %s, t.City = %s, t.State = %s, t.Street =
        %s, t.Last_Name = %s, t.Postal_Code = %s, t.Address_id = %s WHERE t.Address_id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp
#
# @app.route('/api/v1/cities', methods=['POST'])
# def api_add() -> str:
#
#     content = request.json
#
#     cursor = mysql.get_db().cursor()
#     inputData = (content['fldName'], content['fldLat'], content['fldLong'],
#                  content['fldCountry'], content['fldAbbreviation'],
#                  content['fldCapitalStatus'], request.form.get('fldPopulation'))
#     sql_insert_query = """INSERT INTO tblCitiesImport (fldName,fldLat,fldLong,fldCountry,fldAbbreviation,fldCapitalStatus,fldPopulation) VALUES (%s, %s,%s, %s,%s, %s,%s) """
#     cursor.execute(sql_insert_query, inputData)
#     mysql.get_db().commit()
#     resp = Response(status=201, mimetype='application/json')
#     return resp
#
# @app.route('/api/v1/cities/<int:city_id>', methods=['DELETE'])
# def api_delete(city_id) -> str:
#     cursor = mysql.get_db().cursor()
#     sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
#     cursor.execute(sql_delete_query, city_id)
#     mysql.get_db().commit()
#     resp = Response(status=200, mimetype='application/json')
#     return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
