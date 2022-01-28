from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('presen.html')

@app.route('/j', methods=["GET", "POST"])
def js_test():
	if request.method == "POST":
		data = request.form['data']
		p.show()

if __name__ == '__main__':
	app.run(debug=True)