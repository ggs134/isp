#-*-coding:utf-8-*-

# all the import
from sqlalchemy import create_engine, desc, asc, func
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, request, redirect, url_for, abort, render_template, flash, jsonify
from flask import session as login_session
from json import dumps, loads
from sqlalchemy.ext.declarative import declarative_base
import sys

# DB fils import
from isp_final import Base, Department , Dept_obj, Object

#configuration
# DEBUG = True
# SECRET_KEY = '1234'
# USERNAME = 'adminJ'
# PASSWORD = 'wjdtnsgud1!'

#create our little application
app=Flask(__name__)
app.config.from_object(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')

#Connect to Database and create database session
engine = create_engine("mysql://root:wjdtnsgud1!@localhost/isp", encoding='utf8', echo=False)
Base.metadata.bind = engine
DBSession=scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = DBSession()

#deportment
#@app.route('/')
#def show_deportment():
	# entries=session.query(Entries).order_by(desc(Entries.id)).all()
	# session.close()
	#return jsonify(greeting= 'Hello ISP!')

#Deportment
@app.route('/department')
def show_department():
	query = session.query(Department)
	query_list =  query.all()
	converted_list = []
	for i in query_list:
		individual_object = i.__dict__.copy()
		del individual_object['_sa_instance_state']
		converted_list.append(individual_object)
	return jsonify(results = converted_list)

#Department Read
@app.route('/department', methods=['GET','POST','PUT','DELETE'])
def show_department():
	if request.method == "POST":
	 	#Get Request
	 	data = request.get_json(force=True)
	 	#get data from requested
	 	idf = data['a'].encode('utf-8')
	 	dept_code = data['dept_code'].encode('utf-8')
	 	dept_desc = data['dept_desc'].encode('utf-8')
	 	
		if idf == 'ShowDepartment':
		  	query = session.query(Department)
			query_list = query.from_statement("select * from department where dept_code=:dept_code OR dept_desc=:dept_desc).params(dept_code=dept_code, dept_desc=dept_desc).all()")
			if query_list is not None:
		  		converted_list = []
		  		for i in query_list:
		  			individual_department = i.__dict__.copy()
		  			del individual_department['_sa_instance_state']
		  			converted_list.append(individual_department)
		  		session.close()
		  		return jsonify(results = converted_list)
		  	else:
		  		return jsonify(results = "0")
		elif idf == 'CreateDepartment':
			newDept=Department(dept_code = dept_code, dept_desc = dept_desc)
			session.add(newDept)
			session.commit()
			session.close()
			return jsonify(results = "1")

		elif type(idf) == type("") :
		  	return jsonify(results = 0)

	

	elif request.method==['POST']:
		#Get Request
	 	data = request.get_json(force=True)
	 	#get data from requested
	 	idf = data['a'].encode('utf-8')
	 	dept_code = data['dept_code'].encode('utf-8')
	 	dept_desc = data['dept_desc'].encode('utf-8')

		if idf == 'AddDepartment':
			query = session.query(Department)
			query_list = query.form_statement("insert into table Department values('dept_code=:dept_code','dept_desc=:dept_desc').params(dept_code=dept_code,dept_desc=dept_desc).first()")
			if query_update in None:
				return jsonify(results="0")
			query_update.dept_code = dept_code
			query_update.dept_desc = dept_desc
			# 세션 커밋
			session.commit()
			session.close()
			return jsonify(results = "1")

	# 삭제 수행
	elif request.method==['PUT']:
		data = request.get_json(force=True)
		idf = data['a'].encode('utf-8')
		dept_code = data['dept_code'].encode('utf-8')
	 	dept_desc = data['dept_desc'].encode('utf-8')

		if idf=='UpdateDepartment':
			query = session.query(Department)
			query_update = query.form_statement("Select * from Department where dept_code=:dept_code).params(dept_code=dept_code).first()")			
			if query_update in None:
				return jsonify(results="0")
			query_update.dept_code = dept_code
			query_update.dept_desc = dept_desc
			# 세션 커밋
			session.commit()
			session.close()
			return jsonify(results = "1")

	elif request.method==['DELETE']:
		data = request.get_json(force=True)
		idf = data['a'].encode('utf-8')
		dept_code = data['dept_code'].encode('utf-8')
	 	dept_desc = data['dept_desc'].encode('utf-8')

		if idf=='DeleteDepartment':
			query = session.query(Department)
			query_del = query.form_statement("Select * from Department where dept_code=:dept_code).params(dept_code=dept_code).first()")
			session.delete(query_del)
			session.commit()
			session.close()
			return jsonify(results = "1")
	
	query = session.query(Department)
	query_list = query.all()
	converted_list = []
	for i in query_list:
		individual_Department = i.__dict__.copy()
		del individual_department['_sa_instance_state']
		converted_list.append(individual_department)
	session.close()
	return jsonify(results = converted_list)

if __name__=='__main__':
	app.run(host='0.0.0.0')
	app.debug=True
