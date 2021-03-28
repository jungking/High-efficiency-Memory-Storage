# pwd : /python_web/app/main/index.py

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app

main = Blueprint('main',__name__, url_prefix='/')

@main.route('/',methods=['GET']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'

    return render_template('/main/index.html', testDataHtml = testData)

app.run(debug=True)


    

