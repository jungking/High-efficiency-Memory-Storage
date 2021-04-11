# pwd : /python_web/app/main/index.py

from flask import Blueprint, request, render_template, Flask, redirect, url_for, session
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

app = Blueprint('main', __name__, url_prefix='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    # Create user table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/',methods=['GET','POST']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    if not session.get('logged_in'):
        return render_template('main/index.html', testDataHtml = testData)
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_temmplate('main/index.html', data = getfollowwedby(username))
        return render_template('main/index.html', testDataHtml = testData)

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        return render_template('/sign/signin.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method =='POST':
        new_user = User(username = request.form['username'], password = request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('sign/signin.html')
    return render_template('sign/signup.html')

@app.route('/lognout')
def logout():
    sesesion['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/profile') #프로필 창 들어가기
def profile():
    return render_template('/profile.html')

@app.route('/upload<int:num>') #업로드 창 int값
def datecal(num=None):
    return render_template('/upload.html', num=num)

@app.route('/upload') #업로드 창 들어가기
def datecal1(num=None):
    return render_template('/upload.html', num=num)    

@app.route('/picture') #사진 창 들어가기
def picture():
    return render_template('/picture.html')

@app.route('/picture/prev',methods=['POST']) #프로필탭 이전사진으로
def prev():
    return render_template('/picture.html')

@app.route('/picture/next',methods=['POST']) #프로필탭 다음사진으로
def next():
    return render_template('/picture.html')

@app.route('/upload/calculate',methods=['POST']) # 업로드 계산기
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
    else:
        num=None
    return redirect(url_for('.datecal',num=temp))   # .써라

if __name__ == "__main__":
    db.create_all()
    app.secret_key = "123"
    app.run(debug=True)
    #app.run(debug=True,host="127.0.0.1",port=5000)

