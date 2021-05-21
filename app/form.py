from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from app.model.my_user_model import User

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()]) #비밀번호 확인


class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
            
        def __call__(self, form, field):
            user = form['userid'].data
            pwd = form['password'].data
            
            usertable = User.query.filter_by(userid=user,password=pwd).first()
            
            if usertable is None:
            	raise ValueError('아이디 또는 비밀번호가 틀림')
                
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])