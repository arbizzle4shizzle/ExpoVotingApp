from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

voterPassword = "vote123"

@app.route('/', methods = ['GET', 'POST'])
def login():
    return render_template('voterLogin.html')

@app.route('/authenticate', methods = ['GET', 'POST'])
def user_auth():
    password = request.form['passField']
    if (password != voterPassword):
        return redirect(url_for('incorrectLogin'))
    return redirect(url_for('welcomeScreen'))

@app.route('/incorrectLogin')
def incorrectLogin():
    return 'Your Login information was incorrect. Please try again'

@app.route("/welcome", methods=['GET', 'POST'])
def welcomeScreen():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def voting():
	print('In vote.py')
	return render_template('results.html')

if __name__ == '__main__':
    app.run(debug = True)