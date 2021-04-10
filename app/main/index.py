# pwd : /python_web/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app

main = Blueprint('main',__name__, url_prefix='/')

@main.route('/',methods=['GET']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    return render_template('main/index.html', testDataHtml = testData)

@main.route('/profile') #프로필 창 들어가기
def profile():
    return render_template('/profile.html')

@main.route('/upload<int:num>') #업로드 창 int값
def datecal(num=None):
    return render_template('/upload.html', num=num)

@main.route('/upload') #업로드 창 들어가기
def datecal1(num=None):
    return render_template('/upload.html', num=num)    

@main.route('/picture') #사진 창 들어가기
def picture():
    return render_template('/picture.html')

@main.route('/picture/prev',methods=['POST']) #프로필탭 이전사진으로
def prev():
    return render_template('/picture.html')

@main.route('/picture/next',methods=['POST']) #프로필탭 다음사진으로
def next():
    return render_template('/picture.html')


@main.route('/upload/calculate',methods=['POST']) # 업로드 계산기
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
    else:
        num=None
    return redirect(url_for('.datecal',num=temp))   # .써라



