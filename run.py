# pwd : python_web/run.py

from app.app import app

if __name__ == "__main__":

    app.run(debug=True)
    #app.run(debug=True,host="127.0.0.1",port=5000)




