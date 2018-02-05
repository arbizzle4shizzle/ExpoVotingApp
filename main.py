from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

voterPassword = "vote123"

#question is the header for the voting page
#fields are each of the voting option titles
poll_data = {
   'question' : 'Vote on a Project',
   'fields'   : ['Project 1', 'Project 2', 'Project 3', 'Project 4', 'Project 5']
}
#filename for mock database
filename = 'data.txt'

#Displays Login Page for voters
@app.route('/', methods = ['GET', 'POST'])
def login():
    #Renders voterLogin.html
    return render_template('voterLogin.html')

#Checks password and redirects to necessary url
@app.route('/authenticate', methods = ['GET', 'POST'])
def user_auth():
    #checks if inputted password is correct
    password = request.form['passField']
    #if password is wrong, redirect user to incorrectLoginScreen
    if (password != voterPassword):
        return redirect(url_for('incorrectLoginScreen'))
    #after logging in, go to pollScreen
    return redirect(url_for('pollScreen')) 

#Displays failed login page
@app.route('/incorrectLoginScreen')
def incorrectLoginScreen():
    #renders incorrectLogin.html
    return render_template('incorrectLogin.html')

#Displays voting options page
@app.route('/pollScreen')
def pollScreen():
    #renders poll.html and passes poll_data to template
    return render_template('poll.html', data = poll_data)

#Display page after voting is complete
@app.route('/submitted')
def poll():
    vote = request.args.get('field')

    out = open(filename, 'a')
    out.write( vote + '\n' )
    out.close()

    return render_template('thankyou.html', data = poll_data)

#Displays results page
@app.route('/results', methods=['GET', 'POST'])
def voting():
    #initialize votes dict
    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0
    #read votes from mock database
    f = open(filename, 'r')
    for line in f:
        vote = line.rstrip()
        votes[vote] += 1
    #display results.html pass in project names and number of votes
    return render_template('results.html', data=poll_data, votes=votes)

#main method
if __name__ == '__main__':
    app.run(debug = True)
