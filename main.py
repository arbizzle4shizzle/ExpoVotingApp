from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

voterPassword = "vote123"

poll_data = {
   'question' : 'Vote on a Project',
   'fields'   : ['Project 1', 'Project 2', 'Project 3', 'Project 4', 'Project 5']
}

filename = 'data.txt'

@app.route('/', methods = ['GET', 'POST'])
def login():
    return render_template('voterLogin.html')

@app.route('/authenticate', methods = ['GET', 'POST'])
def user_auth():
    password = request.form['passField']
    if (password != voterPassword):
        return redirect(url_for('incorrectLogin'))
    return redirect(url_for('pollScreen'))

@app.route('/incorrectLogin')
def incorrectLogin():
    return 'Your Login information was incorrect. Please try again'

@app.route("/welcome", methods=['GET', 'POST'])
def welcomeScreen():
    return render_template('index.html')

@app.route('/pollScreen')
def pollScreen():
    return render_template('poll.html', data = poll_data)

@app.route('/poll')
def poll():
    vote = request.args.get('field')

    out = open(filename, 'a')
    out.write( vote + '\n' )
    out.close()

    return render_template('thankyou.html', data = poll_data) 

@app.route('/results', methods=['GET', 'POST'])
def voting():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0

    f = open(filename, 'r')
    for line in f:
        vote = line.rstrip()
        votes[vote] += 1

    return render_template('results.html', data=poll_data, votes=votes)

if __name__ == '__main__':
    app.run(debug = True)