from __future__ import print_function
from flask import Flask, g, render_template, request, redirect, session, url_for
from flaskext.mysql import MySQL
import collections
import operator
import io
import csv
import os
import time
import sys

app = Flask(__name__)

#voterPassword = "vote123"
#organizerPassword = "organizer123"

#secret key required for keeping track of user sessions
app.secret_key = 'D8K27qBS8{8*sYVU>3DA530!0469x}'

#question is the header for the voting page
#fields are each of the voting option titles
poll_data = {
   'question' : 'Vote on a Project',
   'projects'   : {}
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
    get_cursor().execute("SELECT `Role` FROM `User` WHERE `Password`=%s", [password])
    role = get_cursor().fetchone()
    if role is not None:
        role = role[0]
        session['username'] = role
    #if password is wrong, redirect user to incorrectLoginScreen
    if role == 'Attendee':
        #after logging in, go to pollScreen
        return redirect(url_for('pollScreen'))
    elif role == 'Organizer':
        return redirect(url_for('organizerScreen'))
    else:
        return redirect(url_for('incorrectLoginScreen'))

#Displays project upload page
@app.route('/uploadProjects', methods = ['GET', 'POST'])
def uploadProjects():
    #renders upload.html
    return render_template('uploadProjects.html')

#Logic for converting a a csv file into entries in the database
@app.route('/uploader', methods = ['GET', 'POST'])
def uploadProjectsToDatabase():
    # Checks if a post request was made to this url
    # If so, checks for the uploaded file
    if request.method == 'POST':
        # Grabs the uploaded file
        f = request.files['file']
        # Creates a stream from the data in the csv
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        # The first row of the csv file is the name of the columns of the database
        columns = next(csv_input)
        query = '''INSERT INTO Project({0}) VALUES ({1})'''
        query = query.format(','.join(columns), ','.join(list(('%s',) * len(columns))))
        addedProjects = []
        for data in csv_input:
            teamNum = data[0]
            projName = data[2]
            try:
                get_cursor().execute(query, data)
                get_db().commit()
                get_cursor().close()
                addedProjects.append("Team " + teamNum + ": " + projName)
            except:
                pass
        return render_template("showUploadedProjects.html", data = addedProjects)

#Displays failed login page
@app.route('/incorrectLoginScreen', methods=['GET', 'POST'])
def incorrectLoginScreen():
    #renders incorrectLogin.html
    return render_template('incorrectLogin.html')

#Displays voting options page
@app.route('/pollScreen', methods=['GET', 'POST'])
def pollScreen():
    # Clear the poll_data projects in case any have been removed during this session
    poll_data['projects'].clear()
    # Create a cursor for the database
    try:
        # Grab the TeamNum and ProjName from all the projects in the database
        get_cursor().execute("SELECT `TeamNumber`,`TeamName`,`ProjName`, `Description` FROM `Project`")
        for (teamNum, teamName, projName, descript) in get_cursor():
            # Checking if the teamNum and projName are present
            if (teamNum != None and projName != None):
                # Converting utf-8 teamNum and projName to normal strings
                # Adding {teamNum : projName} to dictionary
                poll_data['projects'][str(teamNum)] = [str(teamNum),str(teamName),str(projName), str(descript)]
    except:
        pass
    '''
    TODO: Check if there are 0 results returned and show a different html
    or show a message explaining this on the poll.html page
    '''
    # Ordering the projects by team number
    poll_data['projects'] = collections.OrderedDict(sorted(poll_data['projects'].items()))
    # renders poll.html and passes poll_data to template
    return render_template('poll.html', data = poll_data)

@app.route('/commentSubmitted',methods=['GET','POST'])
def commentSubmitted():
    teamNumber = request.args.get('teamNumber')
    commentText = request.form["comment"]
    tStamp = time.time()
    print(teamNumber,file=sys.stderr)
    print(commentText,file=sys.stderr)
    # try:
    get_cursor().execute("INSERT INTO `Comment` (TeamNum,TimeStamp,Text) VALUES (teamNumber,tStamp,commentText)");
    get_db().commit()
    get_cursor().close()
    # except:
    #     pass
    return render_template('thankyou.html')    

#Display page after voting is complete
@app.route('/submitted', methods=['GET', 'POST'])
def poll():
    # Getting the team number the person voted for
    votedTeamNum = request.args.get('field')
    # Using boolean to check if vote was recorder
    voteRegistered = False
    try:
        # Grabbing NumVotes for selected project
        get_cursor().execute("SELECT `NumVotes` FROM `Project` WHERE `TeamNumber` = %s", [votedTeamNum])
        currNumVotes = get_cursor().fetchone()
        if currNumVotes is not None:
            currNumVotes = currNumVotes[0]
        # Adding one vote to the selected project
        get_cursor().execute("UPDATE `Project` SET `NumVotes` = %s WHERE `TeamNumber` = %s", [currNumVotes + 1, votedTeamNum])
        get_db().commit()
        get_cursor().close()
        voteRegistered = True
    except:
        pass
    return render_template('thankyou.html', data = votedTeamNum, goodVote = voteRegistered)

#Displays results Page
@app.route('/results', methods=['GET', 'POST'])
def voting():
    #disallow access for regular attendees
    if session['username'] != 'Organizer':
        return render_template('invalidAccess.html')
    # Clear the poll_data projects in case any have been removed during this session
    poll_data['projects'].clear()
    # Creating a dictionary to store team vote data
    votes = {}
    try:
        # Grab the TeamNum, ProjName, and NumVotes from all the projects in the database
        get_cursor().execute("SELECT `TeamNumber`,`ProjName`,`NumVotes` FROM `Project`")
    except:
        pass
    for (teamNum, projName, numVotes) in get_cursor():
        # Checking if the teamNum, projName, and numVotes are present
        if (teamNum != None and projName != None and numVotes != None):
            # Converting utf-8 teamNum and projName to normal strings, and numVotes to int
            # Adding {teamNum : projName} to projects dictionary
            poll_data['projects'][str(teamNum)] = str(projName)
            # Adding {teamNum : numVotes} to votes dictionary
            votes[str(teamNum)] = numVotes
    '''
    TODO: Check if there are 0 results returned and show a different html
    or show a message explaining this on the results.html page
    '''
    # Ordering the projects by number of votes
    votes = sorted(votes.items(), key=operator.itemgetter(1), reverse=True)
    print(votes)
    #display results.html pass in project names and number of votes
    return render_template('results.html', data=poll_data, votes=votes)

#Displays organizer homepage
@app.route('/organizerScreen', methods=['GET', 'POST'])
def organizerScreen():
    #renders organizerHome.html
    return render_template('organizerHome.html')

#Displays results Page
@app.route('/comments', methods=['GET', 'POST'])
def viewComments():
    #disallow access for regular attendees
    if session['username'] != 'Organizer':
        return render_template('invalidAccess.html')
    try:
        # Creating a dictionary to store team comment data
        # comments = {teamNum: [comment1, comment2, ...]}
        comments = {}
        # Grab comment data from the database
        get_cursor().execute("SELECT `TeamNum`, `TimeStamp`,`Text` FROM `Comment`")
        for (teamNum, timeStamp, text) in get_cursor():
            # Checking if the teamNum and text are present
            if (teamNum != None and text != None):
                # if the team is already in the dict 
                if teamNum in comments:
                    # append the comment to the comment list
                    comments[teamNum].append(text)
                # if the team is not in the dict
                else:
                    # add the team to the dict and create the comment list
                    comments[teamNum] = [text]
    except Exception as e:
        print(e)
        pass

    # Ordering the comments by team number
    comments = collections.OrderedDict(sorted(comments.items()))

    #display comments.html 
    return render_template('comments.html', data=comments)

#main method
if __name__ == '__main__':
    app.run(debug = True)
