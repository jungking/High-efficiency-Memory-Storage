import os.path
from flaskext.mysql import MySQL
from flask import request, Flask,flash, session, render_template, redirect, url_for
import base64
from io import BytesIO
from PIL import Image
import datetime

from pymysql import NULL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kh12241224'
app.config['MYSQL_DATABASE_DB'] = 'flask_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

image_num, n = 0, 0
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
            session['logflag'] = 'logged in'
            session['userid'] = userid
            print(session['logflag'])
            print(session['userid'],"으로 로그인 성공")
            return redirect('/')
        else:
            error = '아이디나 패스워드가 틀립니다.'
            return render_template('sign/signin.html',error=error)

@app.route('/signup', methods=['GET','POST'])
def signup():
    error = None
    if request.method == 'GET':
        return render_template("sign/signup.html")
    else:
        userid = request.form['userid']
        password = request.form['password']
        subd = datetime.datetime.now().strftime("%Y-%m-%d")
        print(subd)
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
            sql = "INSERT INTO user_table(userid, password, sub_date) VALUES('%s', '%s', '%s')" %(userid,password,subd)
            cursor.execute(sql)
            data = cursor.fetchall()

            #cursor.close()
            #conn.close()

            if not data:
                conn.commit()
                return redirect(url_for('index'))
            else:
                conn.rollback()
                print("회원가입 실패")
                return render_template('sign/signup.html')

@app.route('/nav')
def nav(userid):
    return render_template('main/nav.html', userid = userid)

@app.route('/logout')
def logout():
    session.pop('userid',None)
    session['logflag'] = 'logged out'
    print(session['logflag'])
    return redirect('/')

@app.route('/profile',methods=['POST','GET']) #프로필 창 들어가기
def profile():
    conn = mysql.connect()
    cursor = conn.cursor()
    userid = session['userid']
    sql = "SELECT sub_date FROM user_table WHERE userid = %s"
    value = (userid)
    cursor.execute(sql,value)
    timedata = cursor.fetchone()
    print(timedata[0])
    return render_template('/profile.html',timedata = timedata[0])

@app.route('/upload', methods = ['GET', 'POST']) #업로드 창 들어가기
def datecal():
    if request.method =='GET':
        return render_template("upload.html")
    else:
        date = request.form['date']
        file = request.files['file']
        user_id = session['userid']
        content = request.form['content']

        buffer = BytesIO()
        img = Image.open(file)
        img.save(buffer, format="png")
        img_str = base64.b64encode(buffer.getvalue())
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "SELECT MAX(sub_id) FROM picture_table WHERE userid = %s"
        cursor.execute(sql,(user_id))
        sub_id = cursor.fetchone()
        
        if None in sub_id :
            sub_id = 1
        else:
            sub_id = sub_id[0]
            sub_id = sub_id + 1

        sql = "INSERT INTO picture_table(sub_id,date,pic,userid,content) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql,(sub_id,date,img_str,user_id,content))
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
    user_id = session['userid']
    sql = "SELECT pic, content FROM picture_table WHERE userid = %s"
    value = (user_id)
    cursor.execute(sql,value)
    image = cursor.fetchall()
    #print(image)
    global image_num
    global n
    image_num = n
    #print(session['seeall'])
    get_image_all = []
    get_content_all = []
    get_image = 0
    get_content = 0

    if session['seeall'] == 1:
        for i in range(image_num):
            get_image_all.append(image[i][0])
            get_content_all.append(image[i][1])
            get_image_all[i] = get_image_all[i].decode("UTF-8") 
            print('zzzzzzzzz')
            print(get_content_all)   
    else:
        get_image = image[image_num][0]                 # 2차원 튜플 형식                   # 0번째 이미지 출력
        get_content = image[image_num][1]
        get_image = get_image.decode("UTF-8")

    cursor.close()
    conn.close()
    return render_template('/picture.html',get_image=get_image, get_content = get_content, get_image_all = get_image_all, get_content_all = get_content_all)

@app.route('/picture/seeall',methods=['POST']) #프로필탭 이전사진으로`
def seeall():
    session['seeall'] = 1
    return redirect('/picture')


@app.route('/picture/prev',methods=['POST']) #프로필탭 이전사진으로`
def prev():
    global image_num
    global n
    session['seeall'] = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    user_id = session['userid']
    sql = "SELECT id FROM picture_table WHERE userid = %s"
    value = (user_id)
    cursor.execute(sql,value)

    if (image_num == 0):
        flash("가장 처음 사진입니다.")
        print("가장 처음")
        return redirect('/picture')
    else:
        n = image_num-1
        image_num = n
        return redirect('/picture')

@app.route('/picture/next',methods=['POST']) #프로필탭 다음사진으로
def next():
    global image_num
    global n
    session['seeall'] = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    user_id = session['userid']
    sql = "SELECT id FROM picture_table WHERE userid = %s"
    value = (user_id)
    cursor.execute(sql,value)
    num = [item[0] for item in cursor.fetchall()]

    if (image_num == len(num)-1):
        flash("가장 마지막 사진입니다.")
        print("가장 마지막")
        image_num = image_num
        return render_template('/picture.html')
    else:
        n = image_num+1
        image_num = n
        return redirect('/picture')

app.run(debug=True,host="127.0.0.1",port=5000)