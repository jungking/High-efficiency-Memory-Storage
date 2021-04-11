# pwd : /python_web/app/__init.py__

from flask import Flask

app = Flask(__name__)

from app.main.index import app as main
app.register_blueprint(main)
