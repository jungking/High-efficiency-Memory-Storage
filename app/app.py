import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask import request, Flask, session, render_template, redirect, url_for
from .model.my_user_model import User
from .model.my_user_model import Picture
from .model.my_user_model import db
from .form import *
import sys

app = Flask(__name__)
app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

@app.route('/',methods=['GET','POST']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    """if not session.get('logflag'):
        return render_template('main/index.html', testDataHtml = testData)
    else:
        if request.method == 'POST':
            userid = getname(request.form['userid'])
            return render_template('main/index.html', data = getfollowedby(userid))     """
    
    return render_template('main/index.html', testDataHtml = testData)

@app.route('/signin', methods=['GET','POST'])
def signin():
    form = LoginForm() #로그인폼
    if form.validate_on_submit(): #인증
        name = form.data.get('userid')
        print('{}가 로그인 했습니다'.format(name))
        session['userid']=form.data.get('userid') #form에서 가져온 userid를 세션에 저장
        session['logflag'] = 1
        return redirect('/') #성공하면 main.html로
    return render_template('sign/signin.html',form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template("sign/signup.html")
    else:
        userid = form.data.get('userid')
        password = form.data.get('password')
        if not(userid and password):
            return "입력 필수"
        if(userid and password):
            usertable = User()
            usertable.userid = userid
            usertable.password = password
            
            db.session.add(usertable)
            db.session.commit()

            session['user'] = userid

            return redirect('/')
        return render_template('sign/signup.html',form=form)

@app.route('/nav')
def nav(userid):
    return render_template('main/nav.html', userid = userid)

@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('logflag',None)
    return redirect('/')

@app.route('/profile') #프로필 창 들어가기
def profile():
    return render_template('/profile.html')

@app.route('/upload', methods = ['GET', 'POST']) #업로드 창 들어가기
def datecal(date=None):
    if request.method =='GET':
        return render_template("upload.html")
    else:
        date = request.form['date']
        print(date)
        pictable = Picture()
        pictable.date = date
        pictable.pic = 1
        db.session.add(pictable)
        db.session.commit()
    return render_template('/upload.html')    

@app.route('/picture') #사진 창 들어가기
def picture():
    return render_template('/picture.html')

@app.route('/picture/prev',methods=['POST']) #프로필탭 이전사진으로`
def prev():
    return render_template('/picture.html')

@app.route('/picture/next',methods=['POST']) #프로필탭 다음사진으로
def next():
    return render_template('/picture.html')

#데이터베이스---------
basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다


#csrf = CSRFProtect()
#csrf.init_app(app)

db.init_app(app) #app설정값 초기화
db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
db.create_all() #DB생성

   
#app.run(debug=True)
app.run(debug=True,host="127.0.0.1",port=5000)

