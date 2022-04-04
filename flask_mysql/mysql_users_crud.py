#  mysql.connector
#  sqlalchemy sqlite
from flask import Flask
# from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import pymysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash

from flaskext.mysql import MySQL

mysql = MySQL()
 
app = Flask(__name__)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'roytuts'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



data = pd.read_csv ('users.csv')   
df = pd.DataFrame(data)

def init():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()

		cursor.execute('''
				CREATE TABLE IF NOT EXISTS tbl_user (
					userId int primary key,
					name nvarchar(50),
					city nvarchar(50),
					locations nvarchar(50)
					)
					''')
		conn.commit()

		for index, (u, n, c, l) in df.iterrows():
			cursor.execute('''
				INSERT into tbl_user values (
					%s, %s, %s, %s
					)
					''', (u,n,c,l))
			conn.commit()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
# @app.route('/add', methods=['POST'])
# def add_user():
# 	try:
# 		_json = request.json
# 		_name = _json['name']
# 		_email = _json['email']
# 		_password = _json['pwd']
# 		# validate the received values
# 		if _name and _email and _password and request.method == 'POST':
# 			#do not save password as a plain text
# 			_hashed_password = generate_password_hash(_password)
# 			# save edits
# 			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
# 			data = (_name, _email, _hashed_password,)
# 			conn = mysql.connect()
# 			cursor = conn.cursor()
# 			cursor.execute(sql, data)
# 			conn.commit()
# 			resp = jsonify('User added successfully!')
# 			resp.status_code = 200
# 			return resp
# 		else:
# 			return not_found()
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close() 
# 		conn.close()
		
@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user WHERE userId=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['userId']
		_name = _json['name']
		_city = _json['city']
		_locations = _json['locations']		
		# validate the received values
		if _name and _city and _locations and _id and request.method == 'POST':
			# save edits
			sql = "UPDATE tbl_user SET name=%s, city=%s, locations=%s WHERE userId=%s"
			data = (_name, _city, _locations, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			cursor.close()
			conn.close()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE userId=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
	message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
	resp = jsonify(message)
	resp.status_code = 404
	return resp

if __name__ == '__main__':
	# init()
	app.run()  # run our Flask app