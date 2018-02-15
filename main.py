from flask import Flask, g, render_template, request, redirect, session, url_for
from flaskext.mysql import MySQL
import os

app = Flask(__name__)

voterPassword = "vote123"
organizerPassword = "organizer123"

#question is the header for the voting page
#fields are each of the voting option titles
poll_data = {
   'question' : 'Vote on a Project',
   'fields'   : ['Project 1', 'Project 2', 'Project 3', 'Project 4', 'Project 5']
}
#filename for mock database
filename = 'data.txt'

#Information for database connection
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sql9219692'
app.config['MYSQL_DATABASE_PASSWORD'] = '5M2YS1HZdZ'
app.config['MYSQL_DATABASE_DB'] = 'sql9219692'
app.config['MYSQL_DATABASE_HOST'] = 'sql9.freemysqlhosting.net'
mysql.init_app(app)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = mysql.connect()

    return g.mysql_db

def get_cursor():
    """Gets a cursor we can use to point to results in the database"""
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = mysql.connect()

    if not hasattr(g, 'cursor'):
        g.cursor = g.mysql_db.cursor()

    return g.cursor

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()


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
    get_cursor().execute("SELECT `Role` FROM `User` WHERE `password`=%s", [password])
    role = get_cursor().fetchone()
    if role is not None:
        role = role[0]
    #if password is wrong, redirect user to incorrectLoginScreen
    if (role == 'Attendee'):
        #after logging in, go to pollScreen
        return redirect(url_for('pollScreen'))
    elif (role == 'Organizer'):
        return render_template('organizerHome.html')
    else:
        return redirect(url_for('incorrectLoginScreen'))
    
#Displays project upload page
@app.route('/uploadProjects', methods = ['GET', 'POST'])
def upload_projects():
    #renders upload.html
    #TODO: make upload.html page
    return render_template('uploadProjects.html')

# #Logic for converting a a csv file into entries in the database
# @app.route('/submittedProjects')
# def importProjects():
#     # csv file contains column names in first line
#     fileName = 'test.csv'
#     with open (fileName, 'r') as f:
#         reader = csv.reader(f)
#         columns = next(reader) 
#         query = 'insert into MyTable({0}) values ({1})'
#         query = query.format(','.join(columns), ','.join('?' * len(columns)))
#         cursor = connection.cursor()
#         for data in reader:
#             cursor.execute(query, data)
#         cursor.commit() 

# #TODO: Implement this method
# #Shows projects the person just uploaded (or could take them to the vote screen?)
# @app.route('/showProjects')
# def showProjects():
#     pass

#Displays failed login page
@app.route('/incorrectLoginScreen', methods = ['GET', 'POST'])
def incorrectLoginScreen():
    #renders incorrectLogin.html
    return render_template('incorrectLogin.html')

#Displays voting options page
@app.route('/pollScreen', methods = ['GET', 'POST'])
def pollScreen():
    #renders poll.html and passes poll_data to template
    return render_template('poll.html', data = poll_data)

#Display page after voting is complete
@app.route('/submitted', methods = ['GET', 'POST'])
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
