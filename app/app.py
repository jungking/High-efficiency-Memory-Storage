from flaskext.mysql import MySQL
from flask import request, Flask,flash, session, render_template, redirect, url_for, make_response
import datetime
from .ai import show_image
from pymysql import NULL
import random
import os
from PIL import Image

mysql = MySQL()
app = Flask(__name__)

""" app.config['MYSQL_DATABASE_USER'] = 'b82569f91335c3'
app.config['MYSQL_DATABASE_PASSWORD'] = '14c535f1'                  #heroku..
app.config['MYSQL_DATABASE_DB'] = 'heroku_1cef3fce133039c'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-03.cleardb.com' """

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kh12241224'   
app.config['MYSQL_DATABASE_DB'] = 'flask_db'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'


app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

selected_num = 0
mysql.init_app(app)

@app.route('/',methods=['GET','POST']) # /main 으로하면 127.0.0.1:3000/main으로 가야 입력 됨.
def index():
    if 'userid' not in session:
        print('로그인 하세영')
        return render_template('main/index.html')
    else:
        user_id = session['userid']
        conn = mysql.connect()
        cursor = conn.cursor()
    
        sql = "SELECT COUNT(*) FROM picture_table WHERE userid = %s"        #신규가입했는데 에러
        cursor.execute(sql,(user_id))
        conn = cursor.fetchone()
        if conn[0] == 0:                                    
            return render_template('main/index.html')

        sql = "SELECT pic,sub_id FROM picture_table WHERE userid = %s"        
        cursor.execute(sql,(user_id))
        conn = cursor.fetchall()
        get_sub_id=[]
        get_img = []
        for i in range(len(conn)):
            get_img.append(conn[i][0])
            get_sub_id.append(conn[i][1])       
            get_img[i] = get_img[i].decode("UTF-8")
        
        maximum = len(get_sub_id)
        index = random.randint(1,maximum)
        random_image = get_img[index-1]
        newest_image = get_img[maximum-1]

        return render_template('main/index.html', random_image = random_image, newest_image = newest_image)

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
    cursor.execute(sql,(userid))
    timedata = cursor.fetchone()

    sql = "SELECT COUNT(*) FROM picture_table "
    cursor.execute(sql)
    count_all_picture = cursor.fetchone()

    sql = "SELECT COUNT(*) FROM picture_table WHERE userid = %s"
    cursor.execute(sql,(userid))
    count_user_picture = cursor.fetchone()

    sql = "SELECT face,content FROM face_set WHERE userid = %s"
    cursor.execute(sql,(userid))
    data = cursor.fetchall()   
    face = []
    cont = []
    
    for i in range(len(data)):
        face.append(data[i][0])
        cont.append(data[i][1])
        face[i] = face[i].decode('UTF=8")')   # 얼굴 utf 총 모음  cont와 비례
    
    tup_name = []
 
    for i in range(len(cont)):  
        if cont[i] not in tup_name:
            tup_name.append(cont[i])

    tup_face = [[] for i in range(len(tup_name))]

    for i in range(len(cont)):
        for j in range(len(tup_face)):
            if cont[i] == tup_name[j]:
                tup_face[j].append(face[i])

    if count_user_picture[0] == 0:
        return render_template('/profile.html',timedata = timedata[0], count_all_picture = count_all_picture[0], count_user_picture = count_user_picture[0], percent = 0, tup_face=tup_face, tup_name = tup_name)    
    else:
        percent = (count_user_picture[0] / count_all_picture[0])*100
        percent = '%0.1f' % percent
        return render_template('/profile.html',timedata = timedata[0], count_all_picture = count_all_picture[0], count_user_picture = count_user_picture[0], percent = percent, tup_name=tup_name, tup_face = tup_face)

@app.route('/upload', methods = ['GET', 'POST']) #업로드 창 들어가기
def datecal():
    if request.method =='GET':
        return render_template("upload.html")
    else:
        date = request.form['date']
        file = request.files['file']
        user_id = session['userid']
        content = request.form['content']

        conn = mysql.connect()
        cursor = conn.cursor()

        file = file.read()
        face_list=[]
        global face_detect, face_rec
        image, face_detect, face_list, face_rec= show_image(file)
        image = image.decode("UTF=8")   # image
        for i in range(face_detect):
            face_rec[i] = face_rec[i].decode("UTF=8")   # image
        img_str = image

        sql = "SELECT MAX(sub_id) FROM picture_table WHERE userid = %s"
        cursor.execute(sql,(user_id))
        sub_id = cursor.fetchone()

        if None in sub_id :
            sub_id = 1
        else:
            sub_id = sub_id[0] + 1

        sql = "INSERT INTO picture_table(sub_id,date,pic,userid,content) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql,(sub_id,date,img_str,user_id,content))
        data = cursor.fetchall()

        sql = "SELECT content FROM face_set WHERE userid = %s GROUP BY content"
        cursor.execute(sql,(user_id))
        face_data = cursor.fetchall()
        face_content = []
        for i in range(len(face_data)):
            face_content.append(face_data[i][0])

        if not data:
            conn.commit()
            msg = "업로드 성공"
            flash("업로드 성공")
            return render_template('/face.html', img = image ,msg = msg, face_detect = face_detect, face_list = face_list, face_rec = face_rec, face_content = face_content)

        else:
            conn.rollback()
            flash("업로드 실패")
            error = "업로드 실패"
            return render_template('/upload.html',error = error)    

@app.route('/upload/face', methods = ['GET','POST']) #업로드 창 들어가기
def face():
    user_id = session['userid']
    conn = mysql.connect()
    cursor = conn.cursor()

    face_rect = []
    for i in range(face_detect):
        req = request.args.get('face'+ str(i))
        face_rect.append(req)




    for i in range(face_detect):
        sql = "SELECT MAX(sub_id) FROM face_set WHERE userid = %s"
        cursor.execute(sql,(user_id))
        sub_id = cursor.fetchone()

        if None in sub_id :
            sub_id = 1
        else:
            sub_id = sub_id[0] + 1

        sql = "INSERT INTO face_set(sub_id,face,content,userid) VALUES (%s,%s,%s,%s)"        
        cursor.execute(sql,(sub_id,face_rec[i],face_rect[i],user_id))
        data = cursor.fetchall()

    if not data:
        conn.commit()
        flash("업로드 성공")
        return redirect('/upload')

    else:
        conn.rollback()
        flash("업로드 실패")
        error = "업로드 실패"
        return render_template('/upload.html',error = error)    

@app.route('/picture', methods = ['GET','POST']) #사진 창 들어가기
def picture():
    conn = mysql.connect()
    cursor = conn.cursor()
    user_id = session['userid']
    
    sql = "SELECT sub_id, date, pic, content FROM picture_table WHERE userid = %s"        
    #subid, date, pic, content
    value = (user_id)
    cursor.execute(sql,value)
    image = cursor.fetchall()
    global selected_num
    get_image_all = []
    get_content_all = []
    get_subid_all = []
    get_date_all = []
    get_image = 0
    get_content = 0
    num = 0
    num = selected_num
    #if 'seeall' in session:
    for i in range(len(image)):
        get_subid_all.append(image[i][0])       #subid
        get_date_all.append(image[i][1])        #date
        get_image_all.append(image[i][2])       #pic
        get_content_all.append(image[i][3])     #content
        get_image_all[i] = get_image_all[i].decode("UTF-8")
    cursor.close()
    conn.close()
    return render_template('/picture.html',seeall = seeall, num = num, get_image=get_image, get_content = get_content, get_image_all = get_image_all, get_content_all = get_content_all, imagelen= len(get_content_all), get_date_all = get_date_all, get_subid_all = get_subid_all)

@app.route('/picture/seeall',methods=['POST','GET']) #프로필탭 이전사진으로`
def seeall():
    session['seeall'] = 1
    return redirect('/picture')

@app.route('/picture/select_id',methods=['POST','GET'])
@app.route('/num=<int:num>')
def select():
    session.pop('seeall',None)
    global selected_num
    selected_num = int(request.args['num'])
    return redirect(url_for('picture', num = selected_num))

@app.route('/picture/delete',methods=['POST','GET'])
@app.route('/num=<int:num>')
def delete():
    selected_id = int(request.args['num'])
    user_id = session['userid']
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "DELETE FROM picture_table WHERE sub_id = %s AND userid = %s"        
    value = (selected_id, user_id)
    cursor.execute(sql,value)

    conn.commit()
    conn.close()

    print(selected_id, "삭제 완료")
    #subid 삭제
    return redirect('/picture')

app.run(debug=True,host="127.0.0.1",port=int(os.environ.get("PORT",5000)))
#app.run(debug=True)