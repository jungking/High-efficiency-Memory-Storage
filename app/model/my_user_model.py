from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

class User(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'user_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)

    picture = db.relationship('Picture', backref='author',lazy=True)
    #def __init__(self, userid, password):
    #    self.userid = userid
    #    self.set_password(password) 
    
    #def set_password(self, password):
    #    self.password = generate_password_hash(password)

class Picture(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'picture_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    date  = db.Column(db.String(10), nullable=False)
    pic = db.Column(db.String(32), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))

   