from flask import Flask,render_template, request, redirect,send_from_directory
from datetime import datetime

ima = datetime.now()

upload_folder = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/')
def welcome():
    title = "ようこそ"
    page_t = "メインページ"
    time = ima.strftime("%Y年%m月%d日")
    return render_template('index.html',title=title,page_title=page_t,time=time)

@app.route('/midi',methods=["GET","POST"])
def bcmidi():
    title = "midi読み込み"
    page_t = "midi読み込み"
    return render_template('main/bcmidi.html',title=title,page_title=page_t)

@app.route('/key',methods=["GET","POST"])
def bckey():
    title = "キーボード打ち込み"
    page_t = "キーボード打ち込み"
    return render_template('main/bckey.html',title=title,page_title=page_t)

@app.route('/output')
def outputmp3():
    title = "mp3再生"
    page_t = "mp3再生"
    return render_template('main/outputmp3.html',title=title,page_title=page_t)


if __name__ == "__main__":
    app.run(debug=True)