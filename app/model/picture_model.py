from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장

class picdb(db.Model): #데이터 모델을 나타내는 객체 선언
    __tablename__ = 'picture_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    date  = db.Column()
    pic = db.Column(db.String(32), unique=True, nullable=False)


   