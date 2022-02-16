from flask import Flask,render_template, request, redirect,send_from_directory,redirect,url_for
import midi2mp3
from datetime import datetime
from bit_composer import parse_str_to_mid, abc_to_note
from AI.prediction import predict
import locale

upload_folder = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/')
def welcome():
    locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")
    ima = datetime.now()
    title = "ようこそ"
    page_t = "メインページ"
    time = ima.strftime("%Y年%m月%d日")
    return render_template('index.html',title=title,page_title=page_t,time=time)

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

@app.route('/key/syori',methods=["GET","POST"])
def bckeysyori():
    if request.method == "POST":
        moji = request.form['onpu']
        bpm = request.form['bpm']
        int_bpm = int(bpm)
        notes,note_length = abc_to_note(moji)
        predict(notes, note_length,int_bpm)
        midi2mp3.output()
    return redirect(url_for("outputmp3"))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
