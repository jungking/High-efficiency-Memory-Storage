
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

    