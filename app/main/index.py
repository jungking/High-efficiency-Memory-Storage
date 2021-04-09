# pwd : /python_web/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app

app = Blueprint('main',__name__, url_prefix='/')

@app.route('/') # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    return render_template('main/index.html', testDataHtml = testData)

@app.route('/profile')
def profile():
    return render_template('/profile.html')

@app.route('/date<int:num>')
def datecal(num=None):
    return render_template('/date.html', num=num)

@app.route('/date')
def datecal1(num=None):
    return render_template('/date.html', num=num)    

@app.route('/date/calculate',methods=['POST'])
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
    else:
        num=None
    return redirect(url_for('.datecal',num=temp))   # .써라

