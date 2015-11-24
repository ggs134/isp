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
from isp_final import Base, Department, Dept_obj, Object

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
@app.route('/')
def show_deportment():
	# entries=session.query(Entries).order_by(desc(Entries.id)).all()
	# session.close()
	return jsonify(greeting= 'Hello ISP!')

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

#Object Read
@app.route('/object', methods=['GET','POST','PUT','DELETE'])
def show_object():

	if request.method == "POST":
	 	#Get Request
	 	data = request.get_json(force=True)
	 	#get data from requested
	 	idf = data['a'].encode('utf-8')
	 	obj_code = data['obj_code'].encode('utf-8')
	 	# obj_desc = data['obj_desc'].encode('utf-8')
	 	# obj_priority = data['obj_priority'].encode('utf-8')
	 	obj_desc = data['obj_desc'].encode('utf-8')
	 	obj_priority = data['obj_priority'].encode('utf-8')

		if idf == 'ShowObject':
		  	query = session.query(Object)
			#session = stream의 일종
			#sqlalchemy의 Object클레스
		  	#Select * from where obj_code == obj_code or obj_desc == %obj_desc% or obj_priority == obj_priority
		  	# query_list = query.filter(Object.obj_code == obj_code, Object.obj_desc.like("%"+obj_desc+"%"), Object.obj_priority == obj_priority).all()

		  	#This is needs to be converted complex 'where' condition.
		  	# query_list = query.filter("obj_code =:obj_code").params(obj_code=obj_code).all()
		  	query_list = query.from_statement("select * from object where obj_code=:obj_code OR obj_desc=:obj_desc OR obj_priority=:obj_priority").params(obj_code=obj_code, obj_desc=obj_desc, obj_priority=obj_priority).all()
			#>>>>>>>>>> obj_desc의 쿼리 일부분만 검색, 일부 내용 검색 해도 가능하도록 정규표현식화?, sql, sqlalchemy에서 검색

			# query_list = query.filter(Object.obj_code=obj_code).all()

		  	#Check if there a queried list exists
		  	if query_list is not None:
		  		converted_list = []
		  		for i in query_list:
		  			individual_object = i.__dict__.copy()
		  			del individual_object['_sa_instance_state']
		  			converted_list.append(individual_object)
		  		session.close()
		  		return jsonify(results = converted_list)
		  	else:
		  		return jsonify(results = "0")
		elif idf == 'CreateObject':
			newObj=Object(obj_code = obj_code, obj_desc = obj_desc, obj_priority = obj_priority)
			session.add(newObj)
			session.commit()
			session.close()
			return jsonify(results = "1")

		elif type(idf) == type("") :
		  	return jsonify(results = 0)

	query = session.query(Object)
	query_list = query.all()
	converted_list = []
	for i in query_list:
		individual_object = i.__dict__.copy()
		del individual_object['_sa_instance_state']
		converted_list.append(individual_object)
	session.close()
	return jsonify(results = converted_list)

#Object Create
@app.route('/object/add', methods=['POST'])
def add_object():
	#get data
	json_object = request.get_json()
	#parse into variable
	code = json_object['obj_code'].encode('utf-8')
	desc = json_object['obj_desc'].encode('utf-8')
	priority = json_object['obj_priority'].encode('utf-8')
	#create object
	new_object = Object(obj_code = code, obj_desc = desc, obj_priority = priority)
	session.add(new_object)
	session.commit()
 	session.close()
 	return jsonify(results = 1)

#Object Update
@app.route('/object/update', methods=['POST'])
def update_object():
	#get data
	json_object = request.get_json()
	#parse into variable
	code = json_object['obj_code'].encode('utf-8')
	desc = json_object['obj_desc'].encode('utf-8')
	priority = json_object['obj_priority'].encode('utf-8')
	#create object
	session.query(Object).filter(Object.obj_code == code).update({'obj_desc':desc, 'obj_priority':priority})
	session.close()
	return jsonify(results = 1)

#Object Delete
@app.route('/object/delete', methods=['POST'])
def delete_object():
	#get data
	json_object = request.get_json()
	#parse into variable
	code = json_object['obj_code'].encode('utf-8')
	#delete object
	session.query(Object).filter(Object.obj_code == code).delete()
	session.close()
	return jsonify(results = 1)

#Department-Object
@app.route('/dept-obj')
def show_DeptObj():
	query = session.query(Dept_obj)
	query_list =  query.all()
	converted_list = []
	for i in query_list:
		individual_object = i.__dict__.copy()
		del individual_object['_sa_instance_state']
		converted_list.append(individual_object)
	return jsonify(results = converted_list)


# @app.route('/board1/<int:page_number>')
# def board1(page_number):
# 	#총 글의 갯수를 구함
# 	total_number_writings=int(session.query(func.count('*')).select_from(Board1).scalar())
# 	# 왜 +2를 해야 하지?? 총 페이지 수를 도출
# 	total_page_number=int(total_number_writings/10)+2
# 	if page_number>=total_page_number:
# 		flash('그 페이지는 존재하지 않습니다')
# 		return redirect(url_for('board1', page_number=1))
# 	# count number of writings
# 	# session.query(Entries.id).order_by(desc(Entries.id)).first()
# 	if page_number==None:
# 		page_number=1
# 	writings1=session.query(Board1).order_by(desc(Board1.id)).limit(10).offset((page_number-1)*10).all()
# 	session.close()
# 	return render_template('board1.html', writings1=writings1, page_number=page_number, total_page_number=total_page_number)

# #board2 page
# @app.route('/board2/<int:page_number>')
# def board2(page_number):
# 	#총 글의 갯수를 구함
# 	total_number_writings=int(session.query(func.count('*')).select_from(Board2).scalar())
# 	# 왜 +2를 해야 하지?? 총 페이지 수를 도출
# 	total_page_number=int(total_number_writings/10)+2
# 	if page_number>=total_page_number:
# 		flash('그 페이지는 존재하지 않습니다')
# 		return redirect(url_for('board2', page_number=1))
# 	# count number of writings
# 	# session.query(Entries.id).order_by(desc(Entries.id)).first()
# 	if page_number==None:
# 		page_number=1
# 	writings2=session.query(Board2).order_by(desc(Board2.id)).limit(10).offset((page_number-1)*10).all()
# 	session.close()
# 	return render_template('board2.html', writings2=writings2, page_number=page_number, total_page_number=total_page_number)

# #add new notice
# @app.route('/add', methods=['POST'])
# def add_entry():

# 	newEntry=Entries(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newEntry)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('show_entries'))

# #add new post in board1
# @app.route('/add1', methods=['POST'])
# def add1():
# 	newBoard1=Board1(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newBoard1)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('board1',page_number=1))

# #add new post in board2
# @app.route('/add2', methods=['POST'])
# def add2():
# 	newBoard2=Board2(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newBoard2)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('board2',page_number=1))

# #admin login page
# @app.route('/login', methods=['GET','POST'])
# def login():
# 	error=None
# 	if request.method=='POST':
# 		if request.form['username'] != app.config['USERNAME']:
# 			error='invalid username'
# 		elif request.form['password'] != app.config['PASSWORD']:
# 			error='invalid password'
# 		else:
# 			login_session['logged_in']=True
# 			flash('로그인 되었습니다.')
# 			return redirect(url_for('show_entries'))
# 	return render_template('login.html', error=error)

# #admin logout
# @app.route('/logout')
# def logout():
# 	login_session.pop('logged_in', None)
# 	flash('로그아웃되었습니다.')
# 	return redirect(url_for('show_entries'))

# @app.teardown_request
# def shutdown_session(exception=None):
# 	DBSession.remove()

if __name__=='__main__':
	app.run(host='0.0.0.0')
	app.debug=True
