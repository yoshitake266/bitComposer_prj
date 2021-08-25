from flask import Flask,render_template
from datetime import datetime

ima = datetime.now()

app = Flask(__name__)

@app.route('/')
def welcome():
    tit = "ようこそ"
    page_t = "メインページ"
    time = ima.strftime("%Y年%m月%d日")
    return render_template('index.html',title=tit,page_title=page_t,time=time)

if __name__ == "__main__":
    app.run()