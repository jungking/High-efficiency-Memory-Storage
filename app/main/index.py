# pwd : /python_web/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app

main = Blueprint('main',__name__, url_prefix='/')

@main.route('/',methods=['GET']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    return render_template('/main/index.html', testDataHtml = testData)

@main.route('/profile')
def profile():
    return 'HJ, YW`s Profile'

@main.route('/date<int:num>')
def datecal(num=None):
    return render_template('/main/date.html', num=num)

@main.route('/date')
def datecal1(num=None):
    return render_template('/main/date.html', num=num)    

@main.route('/date/calculate',methods=['POST'])
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
    else:
        num=None
    return redirect(url_for('.datecal',num=temp))   # .써라

