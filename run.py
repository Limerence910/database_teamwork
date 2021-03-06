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


@app.route('/deliveryman', methods=['GET'])
def deliveryman():
    return render_template('deliveryman.html')


@app.route('/food', methods=['GET'])
def food():
    return render_template('food.html')

@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/get_current_user', methods=['GET'])
def get_current_user():
    return username

@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

@app.route('/get_form_list', methods=['GET'])
def get_form_list():
    sql = "select * from Form"
    data = db.session.execute(sql)
    output = []
    for record in data:
        r_data = {}
        r_data['Fnum'] = record.Fnum
        r_data['Rno'] = record.Rno
        r_data['Cno'] = record.Cno

        r_data['Fday'] = record.Fday
        r_data['Ftime'] = record.Ftime
        r_data['Rtel'] = record.Rtel
        r_data['Fstatus'] = record.Fstatus
        r_data['Dno'] = record.Dno
        output.append(r_data)
    return jsonify({'data': output})


@app.route('/update_form', methods=['POST'])
def update_form():
    data = dict(eval(request.get_data()))
    sql = "update Form set Fstatus='{}' where Fnum='{}'".format(
        data['Fstatus'], data['Fnum'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/delete_form', methods=['POST'])
def delete_form():
    data = dict(eval(request.get_data()))
    sql = "delete from Form where Fnum='{}'".format(data['Fnum'])
    sql2 = "delete from Formdetail where Fnum='{}'".format(data['Fnum'])
    try:
        db.session.execute(sql)
        db.session.commit()
        db.session.execute(sql2)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/get_formdetail', methods=['POST'])
def get_formdetail():
    datap = dict(eval(request.get_data()))
    sql = "select * from Formdetail,Food,Restaurant where Formdetail.Fno=Food.Fno and Food.Rno=Restaurant.Rno and Fnum='{}' ".format(datap['Fnum'])
    data = db.session.execute(sql)
    # db.session.commit()
    output = []
    print(data)
    for record in data:
        r_data = {}
        r_data['Fnum'] = record.Fnum
        r_data['Fno'] = record.Fno
        r_data['Fname'] = record.Fname
        r_data['Rname'] = record.Rname
        r_data['Fcount'] = record.Fcount
        output.append(r_data)
    return jsonify({'data': output})



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


@app.route('/update_user', methods=['POST'])
def update_user():
    data = dict(eval(request.get_data()))
    sql = "update Consumer set Cname='{}', Caddr='{}', Cmoney='{}', Cgrade='{}', Cdiscount='{}',CTel='{}' where Cno='{}'".format(
        data['Cname'], data['Caddr'], data['Cmoney'], data['Cgrade'], data['Cdiscount'], data['CTel'], data['Cno'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = dict(eval(request.get_data()))
    sql = "delete from Consumer where Cno='{}'".format(data['Cno'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/add_user', methods=['POST'])
def add_user():
    data = dict(eval(request.get_data()))
    sql = "insert into Consumer(Cno,Cname,Caddr,Cmoney,Cgrade,Cdiscount,CTel,Cpaycode) values ('{}', '{}', '{}', '{}', '{}', '{}','{}','{}')".format(
        data['Cno'], data['Cname'], data['Caddr'], data['Cmoney'], data['Cgrade'], data['Cdiscount'], data['CTel'], data['Cpaycode'])
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
    try:
        data = dict(eval(request.get_data()))
        sql = "update Restaurant set Rname='{}', Radd='{}', Rtype='{}', Rtel='{}', Rgrade='{}' where Rno='{}'".format(
            data['Rname'], data['Radd'], data['Rtype'], data['Rtel'], data['Rgrade'], data['Rno'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/delete_restaurant', methods=['POST'])
def delete_restaurant():
    try:
        data = dict(eval(request.get_data()))
        sql = "delete from Restaurant where Rno='{}'".format(data['Rno'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
    try:
        data = dict(eval(request.get_data()))
        sql = "insert into Restaurant values ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            data['Rno'], data['Rname'], data['Radd'], data['Rtype'], data['Rtel'], data['Rgrade'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/get_deliveryman_list', methods=['GET'])
def get_deliveryman_list():
    sql = "select * from Delivery"
    data = db.session.execute(sql)
    output = []
    for record in data:
        r_data = {}
        r_data['Dno'] = record.Dno
        r_data['Dname'] = record.Dname
        r_data['Dtel'] = record.Dtel
        output.append(r_data)
    return jsonify({'data': output})


@app.route('/update_deliveryman', methods=['POST'])
def update_deliveryman():
    try:
        data = dict(eval(request.get_data()))
        sql = "update Delivery set Dname='{}', Dtel='{}' where Dno='{}'".format(
            data['Dname'], data['Dtel'], data['Dno'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/delete_deliveryman', methods=['POST'])
def delete_deliveryman():
    try:
        data = dict(eval(request.get_data()))
        sql = "delete from Delivery where Dno='{}'".format(data['Dno'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/add_deliveryman', methods=['POST'])
def add_deliveryman():
    try:
        data = dict(eval(request.get_data()))
        sql = "insert into Delivery values ('{}', '{}', '{}')".format(
            data['Dno'], data['Dname'], data['Dtel'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/get_food_list', methods=['GET'])
def get_food_list():
    sql = "select * from Food,Restaurant where Food.Rno = Restaurant.Rno"
    data = db.session.execute(sql)
    output = []
    for record in data:
        r_data = {}
        r_data['Rno'] = record.Rno
        r_data['Fname'] = record.Fname
        r_data['Fno'] = record.Fno
        r_data['Fprice'] = record.Fprice
        r_data['Fgood'] = record.Fgood
        r_data['Rname'] = record.Rname
        output.append(r_data)
    
    return jsonify({'data': output})



@app.route('/insert_food', methods=['POST'])
def insert_food():
    data = dict(eval(request.get_data()))
    print(data)
    sql = "insert into Food(Fno,Fname,Fprice,Fgood,Rno) VALUES('{}','{}','{}','{}','{}')".format(
        data['Fno'], data['Fname'], data['Fprice'], data['Fgood'], data['Rno'])
    print(sql)
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/update_food', methods=['POST'])
def update_food():
    data = dict(eval(request.get_data()))
    sql = "update Food set Fno='{}', Fname='{}', Fprice='{}', Fgood='{}', Rno='{}' where Fno='{}'".format(
        data['Fno'], data['Fname'], data['Fprice'], data['Fgood'], data['Rno'], data['Fno'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/delect_food', methods=['POST'])
def delect_food():
    data = dict(eval(request.get_data()))
    sql = "delete from Food where Fno = '{}' ".format(data['Fno'])
    try:
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/get_account_list', methods=['GET'])
def get_account_list():
    sql = "select * from Account"
    data = db.session.execute(sql)
    output = []
    for record in data:
        r_data = {}
        r_data['Ano'] = record.Ano
        r_data['Apassword'] = record.Apassword
        r_data['APermission'] = record.APermission
        r_data['Aid'] = record.Aid
        output.append(r_data)
    return jsonify({'data': output})


@app.route('/update_account', methods=['POST'])
def update_account():
    try:
        data = dict(eval(request.get_data()))
        sql = "update Account set Aid='{}', Apassword='{}', APermission='{}' where Ano='{}'".format(
            data['Aid'], data['Apassword'], data['APermission'], data['Ano'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/delete_account', methods=['POST'])
def delete_account():
    try:
        data = dict(eval(request.get_data()))
        sql = "delete from Account where Ano='{}'".format(data['Ano'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"


@app.route('/add_account', methods=['POST'])
def add_account():
    try:
        data = dict(eval(request.get_data()))
        sql = "insert into Account values ('{}', '{}', '{}', '{}')".format(
            data['Ano'], data['Apassword'], data['APermission'], data['Aid'])
        db.session.execute(sql)
        db.session.commit()
        return "Succeeded"
    except:
        return "Failed"

if __name__ == '__main__':
    app.run(debug=True)
