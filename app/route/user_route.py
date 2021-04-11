import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import Blueprint, request, Flask, session, render_template, redirect, url_for
from model.my_user_model import 
from form import RegisterForm, LoginForm

router = Blueprint('router',__name__)

@router.route('/',methods=['GET','POST']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    if not session.get('logged_in'):
        return render_template('main/index.html', testDataHtml = testData)
    else:
        if request.method == 'POST':
            userid = getname(request.form['userid'])
            return render_temmplate('main/index.html', data = getfollowwedby(userid))
        return render_template('main/index.html', testDataHtml = testData)

@router.route('/signin', methods=['GET','POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        print('{} is Sign In'.format(form.data.get('userid')))
        session['userid']=form.data.get('userid')
        return redirect('main/index.html')
    return render_template('sign/signin.html', form = form)

@router.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        usertable = User()
        usertable.userid = form.data.get('userid')
        usertable.password = form.data.get('password')

        db.session.add(usertable)
        db.session.commit()
        return redirect('main/index.html')
    return render_template('sign/signup.html', form = form)

@router.route('/logout')
def logout():
    session.pop('userid',None)
    return redirect('/')

@router.route('/profile') #프로필 창 들어가기
def profile():
    return render_template('/profile.html')

@router.route('/upload<int:num>') #업로드 창 int값
def datecal(num=None):
    return render_template('/upload.html', num=num)

@router.route('/upload') #업로드 창 들어가기
def datecal1(num=None):
    return render_template('/upload.html', num=num)    

@router.route('/picture') #사진 창 들어가기
def picture():
    return render_template('/picture.html')

@router.route('/picture/prev',methods=['POST']) #프로필탭 이전사진으로`
def prev():
    return render_template('/picture.html')

@router.route('/picture/next',methods=['POST']) #프로필탭 다음사진으로
def next():
    return render_template('/picture.html')

@router.route('/upload/calculate',methods=['POST']) # 업로드 계산기
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
    else:
        num=None
    return redirect(url_for('.datecal',num=temp))   # .써라


