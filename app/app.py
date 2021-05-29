import os.path
from flaskext.mysql import MySQL
from flask import request, Flask,flash, session, render_template, redirect, url_for
from .model.my_user_model import Picture
from .form import *
import base64
from io import BytesIO
from PIL import Image

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kh12241224'
app.config['MYSQL_DATABASE_DB'] = 'flask_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

mysql.init_app(app)

@app.route('/',methods=['GET','POST']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    testData = 'testData array'
    """if not session.get('logflag'):
        return render_template('main/index.html', testDataHtml = testData)
    else:
        if request.method == 'POST':
            userid = getname(request.form['userid'])
            return render_template('main/index.html', data = getfollowedby(userid))     """
    
    return render_template('main/index.html', testDataHtml = testData)

@app.route('/signin', methods=['GET','POST'])
def signin():
    #form = LoginForm() #로그인폼
    error = None
    if request.method == 'GET':
        return render_template("sign/signin.html")
    else:
        userid = request.form['userid']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "SELECT userid FROM user_table WHERE userid = %s AND password = %s"
        value = (userid, password)

        cursor.execute(sql,value)
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in data:
            data = row[0]
        if data:
            session['logflag'] = 1
            session['userid'] = userid
            print(session['userid'],"으로 로그인 성공")
            return redirect('/')
        else:
            error = '아이디나 패스워드가 틀립니다.'
            return render_template('sign/signin.html',error=error)

        #return redirect('/')
    #return render_template('sign/signin.html',error = error)

@app.route('/signup', methods=['GET','POST'])
def signup():
    #form = RegisterForm()
    error = None
    if request.method == 'GET':
        return render_template("sign/signup.html")
    else:
        userid = request.form['userid']
        password = request.form['password']

        conn = mysql.connect()
        cursor = conn.cursor()
            
        sql = "SELECT userid FROM user_table WHERE userid = %s"
        value = (userid)
        cursor.execute(sql,value)
        redup_data = cursor.fetchall()

        if redup_data:
            error = "이미 등록된 아이디입니다."
            return render_template("sign/signup.html",error=error)
        else:
            sql = "INSERT INTO user_table(userid, password) VALUES('%s', '%s')" %(userid,password)
            cursor.execute(sql)
            data = cursor.fetchall()

            if not data:
                conn.commit()
                return redirect(url_for('index'))
            else:
                conn.rollback()
                return "회원가입 실패"

            cursor.close()
            conn.close()
        return render_template('sign/signup.html',error = error)

@app.route('/nav')
def nav(userid):
    return render_template('main/nav.html', userid = userid)

@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('logflag',None)
    return redirect('/')

@app.route('/profile') #프로필 창 들어가기
def profile():
    return render_template('/profile.html')

@app.route('/upload', methods = ['GET', 'POST']) #업로드 창 들어가기
def datecal():
    if request.method =='GET':
        return render_template("upload.html")
    else:
        date = request.form['date']
        file = request.files['file']
        user_id = session['userid']
        
        buffer = BytesIO()
        img = Image.open(file)
        #img.show()
        img.save(buffer, format="png")
        img_str = base64.b64encode(buffer.getvalue())
        #img_str = binary_image.decode('UTF-8')
        #print(img_str)

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO picture_table(date,pic,user_id) VALUES (%s,%s,%s)"
        cursor.execute(sql,(date,img_str,user_id))
        data = cursor.fetchall()

        if not data:
            conn.commit()
            flash("업로드 성공")
            msg = "업로드 성공"
            return render_template('/upload.html', msg = msg)
        else:
            conn.rollback()
            flash("업로드 실패")
            error = "업로드 실패"
            return render_template('/upload.html',error = error)    

@app.route('/picture') #사진 창 들어가기
def picture():
    
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT pic FROM picture_table limit 1"
    cursor.execute(sql)
    images = cursor.fetchone()
    print(images)
    if images:
        get_image = images['image']
        get_image = get_image.degode("UTF-8")
    cursor.close()
    conn.close()

    return render_template('/picture.html',get_image=get_image)

@app.route('/picture/prev',methods=['POST']) #프로필탭 이전사진으로`
def prev():
    return render_template('/picture.html')

@app.route('/picture/next',methods=['POST']) #프로필탭 다음사진으로
def next():
    return render_template('/picture.html')

#데이터베이스---------
basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다


#csrf = CSRFProtect()
#csrf.init_app(app)

#db.init_app(app) #app설정값 초기화
#db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
#db.create_all() #DB생성

   
#app.run(debug=True)
app.run(debug=True,host="127.0.0.1",port=5000)

