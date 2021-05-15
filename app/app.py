import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask import Blueprint, request, Flask, session, render_template, redirect, url_for
from .model.my_user_model import User
from .model.my_user_model import db
from .form import *

app = Flask(__name__)
app.config['SECRET_KEY']='any secret string'

""" db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)

    def __init__(self,userid, password):
        self.userid = userid
        self.set_password(password) 
 """
 
@app.route('/',methods=['GET','POST']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    if not session.get('logged_in'):
        return render_template('main/index.html', testDataHtml = testData)
    else:
        if request.method == 'POST':
            userid = getname(request.form['userid'])
            return render_template('main/index.html', data = getfollowedby(userid))
        return render_template('main/index.html', testDataHtml = testData)

@app.route('/signin', methods=['GET','POST'])
def signin():
    form = LoginForm() #로그인폼
    if form.validate_on_submit(): #인증
        print('{}가 로그인 했습니다'.format(form.data.get('userid')))
        session['userid']=form.data.get('userid') #form에서 가져온 userid를 세션에 저장
        return redirect('/') #성공하면 main.html로
    return render_template('sign/signin.html',form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        usertable = User('userid','password')
        usertable.userid = form.data.get('userid')
        usertable.password = form.data.get('password')

        db.session.add(usertable)
        db.session.commit()
        
        return "회원가입 성공" 
    return render_template('sign/signup.html', form = form)

@app.route('/logout')
def logout():
    session.pop('userid',None)
    return redirect('/')

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

@app.route('/picture/prev',methods=['POST']) #프로필탭 이전사진으로`
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
    basedir = os.path.dirname(os.path.abspath(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다
    app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

    #csrf = CSRFProtect()
    #csrf.init_app(app)

    #db=SQLAlchemy(app)


    db.init_app(app)
    db.app = app
    db.create_all()

   
    #app.run(debug=True)
    app.run(debug=True,host="127.0.0.1",port=5000)

