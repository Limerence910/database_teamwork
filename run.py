from flask import Flask, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template
from sqlalchemy.sql import func
app = Flask(__name__)
db = SQLAlchemy(app)
username = ""
user_type = -1


class Account(db.Model):  # 创建model，对应数据库中的表
    Ano = db.Column(db.String(9), primary_key=True)
    APermission = db.Column(db.Integer)


@app.route('/', methods=['GET'])
def home():
    global username
    global user_type
    username = ""
    user_type = -1
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    global username
    global user_type
    username = dict(eval(request.get_data()))['username']
    password = dict(eval(request.get_data()))['password']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://' + \
        username + ':' + password + '@sqlserver'  # 修改为自己的
    try:
        Account.query.all()
        return "Succeeded"
    except:
        username = ""
        user_type = -1
        return "Failed"


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/user', methods=['GET'])
def user():
    return render_template('user.html')


@app.route('/restaurant', methods=['GET'])
def restaurant():
    return render_template('restaurant.html')


@app.route('/get_current_user', methods=['GET'])
def get_current_user():
    return username

@app.route('/get_user_list', methods=['GET'])
def get_user_list():
    sql = "select * from Consumer"
    data = db.session.execute(sql)
    output = []
    for record in data:
        r_data = {}
        r_data['Cno'] = record.Cno
        r_data['Cname'] = record.Cname
        r_data['Caddr'] = record.Caddr
        
        r_data['CTel'] = record.CTel
        r_data['Cmoney'] = record.Cmoney
        r_data['Cdiscount'] = record.Cdiscount
        r_data['Cgrade'] = record.Cgrade
        output.append(r_data)
    return jsonify({'data': output})

@app.route('/update_user',methods=['POST'])
def update_user():
    data = dict(eval(request.get_data()))
    sql = "update Consumer set Cname='{}', Caddr='{}', Cmoney='{}', Cgrade='{}', Cdiscount='{}',CTel='{}' where Cno='{}'".format(
        data['Cname'], data['Caddr'], data['Cmoney'], data['Cgrade'], data['Cdiscount'],data['CTel'] ,data['Cno'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"
        
@app.route('/delete_user',methods=['POST'])
def delete_user():
    data = dict(eval(request.get_data()))
    sql = "delete from Consumer where Cno='{}'".format(data['Cno'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"

@app.route('/add_user',methods=['POST'])
def add_user():
    data = dict(eval(request.get_data()))
    sql = "insert into Consumer(Cno,Cname,Caddr,Cmoney,Cgrade,Cdiscount,CTel,Cpaycode) values ('{}', '{}', '{}', '{}', '{}', '{}','{}','{}')".format(
        data['Cno'],data['Cname'],data['Caddr'],data['Cmoney'],data['Cgrade'],data['Cdiscount'],data['CTel'],data['Cpaycode'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/get_restaurant_list', methods=['GET'])
def get_restaurant_list():
    sql = "select * from Restaurant"
    data = db.session.execute(sql)
    output = []
    for record in data:
        r_data = {}
        r_data['Rno'] = record.Rno
        r_data['Rname'] = record.Rname
        r_data['Radd'] = record.Radd
        r_data['Rtype'] = record.Rtype
        r_data['Rtel'] = record.Rtel
        r_data['Rgrade'] = record.Rgrade
        output.append(r_data)
    return jsonify({'data': output})


@app.route('/update_restaurant', methods=['POST'])
def update_restaurant():
    sql = "insert into Restaurant values('SN', '!!', '??', '..', 'PP', 2.0)"
    db.session.execute(sql)
    db.session.commit()
    print("1")
    return "P"


if __name__ == '__main__':
    app.run(debug=True)
