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
import datetime
from flask_mail import Mail, Message
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

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
    elif role == 'Admin':
        return redirect(url_for('adminScreen'))
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
    #disallow access for non-attendees
    if session['username'] != 'Attendee':
        return render_template('invalidAccess.html')
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
    # tStamp = time.time()
    print(teamNumber,file=sys.stderr)
    print(commentText,file=sys.stderr)
    # try:
    get_cursor().execute("INSERT INTO `Comment` (`TeamNum`,`Text`) VALUES (%s,%s)", [teamNumber, commentText]);
    get_db().commit()
    get_cursor().close()
    # except:
    #     pass
    return render_template('thankYouComment.html', data = teamNumber)    

#Display page after voting is complete
@app.route('/submitted', methods=['GET', 'POST'])
def poll():
    #Checking if user has already submitted a vote
    userIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print(userIP)
    f = open("ips.txt", "w")
    f.close()
    #get_cursor().execute("SELECT 'IpAddress' FROM 'IP'")
    #for ip in get_cursor().fetchall():
    #    if ip == userIP:
    #        return render_template('alreadyVoted.html');
    # Getting the team number the person voted for
    votedTeamNum = request.args.get('teamNumber')
    print(votedTeamNum)
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
        voteRegistered = True
        #Add user's IP address to database.
        get_cursor().execute("INSERT INTO `IP` (`IpAddress`) VALUES (%s)", [userIP])
        get_db().commit()
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

#Displays comments Page
@app.route('/comments', methods=['GET', 'POST'])
def viewComments():
    #disallow access for regular attendees
    if session['username'] != 'Organizer':
        return render_template('invalidAccess.html')
    try:
        # Creating a dictionary to store team comment data
        # comments = {teamNum: [[comment1, timestamp1], [comment2, timestamp2], ...]}
        comments = {}
        # Grab comment data from the database
        get_cursor().execute("SELECT `TeamNum`, `TimeStamp`,`Text` FROM `Comment`")
        for (teamNum, timeStamp, text) in get_cursor():
            # Checking if the teamNum and text are present
            if (teamNum != None and text != None and timeStamp != None):
                # if the team is already in the dict 
                if teamNum in comments:
                    # append the comment to the comment list
                    comments[teamNum].append([text, timeStamp])
                # if the team is not in the dict
                else:
                    # add the team to the dict and create the comment list
                    comments[teamNum] = [[text, timeStamp]]
    except Exception as e:
        print(e)
        pass
    
    # Ordering the comments by team number
    comments = collections.OrderedDict(sorted(comments.items()))

    #display comments.html 
    return render_template('comments.html', data=comments)

#Displays delete Page
@app.route('/deleteComments', methods=['GET', 'POST'])
def deleteComments():
    # Getting the comments that were checked
    deletedComments = request.args.getlist('delete')

    deletedComments = map(str, deletedComments)

    for t in deletedComments:
        get_cursor().execute("DELETE FROM `Comment` WHERE `TimeStamp` = " + "'" + t + "'")
        get_db().commit()

    return render_template('deleteComments.html')

#Displays sent comments Page
@app.route('/sendComments', methods=['GET', 'POST'])
def sendComments():
    #disallow access for regular attendees
    if session['username'] != 'Organizer':
        return render_template('invalidAccess.html')
    try:
        # Creating a dictionary to store team comment data
        # comments = {teamNum: [[comment1, timestamp1], [comment2, timestamp2], ...]}
        comments = {}
        # Grab comment data from the database
        get_cursor().execute("SELECT `TeamNum`, `TimeStamp`,`Text` FROM `Comment`")
        for (teamNum, timeStamp, text) in get_cursor():
            # Checking if the teamNum and text are present
            if (teamNum != None and text != None and timeStamp != None):
                # if the team is already in the dict 
                if teamNum in comments:
                    # append the comment to the comment list
                    comments[teamNum].append(text)
                # if the team is not in the dict
                else:
                    # add the team to the dict and create the comment list
                    comments[teamNum] = [text]
        projects = {}
        get_cursor().execute("SELECT `TeamNumber`,`ProfEmail`,`Email1`,`Email2`,`Email3`,`Email4`,`Email5` FROM `Project`")
        for (teamNum, profE, E1, E2, E3, E4, E5) in get_cursor():
            projects[teamNum] = [profE, E1, E2, E3, E4, E5]
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("expovotingappgt@gmail.com", "juniordesign2")
        fromaddr = "expovotingappgt@gmail.com"
        toaddr = "arbermuharemi@gmail.com"
        for team in comments.keys():
            for comment in comments[team]:
                # msg = Message("Below is a comment on your project:\n" + comment,
                #     sender=projects[team][0],
                #     recipients=[projects[team][1], projects[team][2], projects[team][3], projects[team][4], projects[team][5]])
                # print(msg)
                # mail.send(msg)
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Feedback from the Junior Design Expo!"
                body = "Below is a comment an expo visitor left your project:\n" + comment
                msg.attach(MIMEText(body, 'plain'))
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.sendmail("expovotingappgt@gmail.com", "arbermuharemi@gmail.com", msg);
        server.quit()
    except Exception as e:
        print(e)
        pass

    return render_template('sendComments.html')

#Displays admin homepage
@app.route('/adminScreen', methods=['GET', 'POST'])
def adminScreen():
    #renders adminHome.html
    return render_template('adminHome.html')

#Checks password and redirects to necessary url
@app.route('/changeAttendeePass', methods = ['GET', 'POST'])
def changeAttendeePass():
    #checks if inputted password is correct
    password = request.form['oldAttendeePass']
    get_cursor().execute("SELECT `Role` FROM `User` WHERE `Password`=%s", [password])
    role = get_cursor().fetchone()
    if role is not None:
        role = role[0]
    #if password is wrong, redirect user to notValidPassScreen
    if role == 'Attendee':
        #after logging in, go to pollScreen
        newPass = request.form['newAttendeePass']
        confirmNewPass = request.form['newAttendeePassConfirm']
        if (newPass == confirmNewPass):
            get_cursor().execute("UPDATE `User` SET `Password` = %s WHERE `Role` = 'Attendee' ", [newPass])
            get_db().commit()
            #get_cursor().close()
            return redirect(url_for('changedAttendeePass'))
        else:
            return redirect(url_for('passwordsDontMatch'))
    else:
        return redirect(url_for('notValidPass'))

#Checks password and redirects to necessary url
@app.route('/changeOrganizerPass', methods = ['GET', 'POST'])
def changeOrganizerPass():
    #checks if inputted password is correct
    password = request.form['oldOrganizerPass']
    get_cursor().execute("SELECT `Role` FROM `User` WHERE `Password`=%s", [password])
    role = get_cursor().fetchone()
    if role is not None:
        role = role[0]
    #if password is wrong, redirect user to notValidPassScreen
    if role == 'Organizer':
        #after logging in, go to pollScreen
        newPass = request.form['newOrganizerPass']
        confirmNewPass = request.form['newOrganizerPassConfirm']
        if (newPass == confirmNewPass):
            get_cursor().execute("UPDATE `User` SET `Password` = %s WHERE `Role` = 'Organizer' ", [newPass])
            get_db().commit()
            #get_cursor().close()
            return redirect(url_for('changedOrganizerPass'))
        else:
            return redirect(url_for('passwordsDontMatch'))
    else:
        return redirect(url_for('notValidPass'))

@app.route('/changedAttendeePass', methods = ['GET', 'POST'])
def changedAttendeePass():
    return render_template("changedAttendeePassScreen.html")

@app.route('/changedOrganizerPass', methods = ['GET', 'POST'])
def changedOrganizerPass():
    return render_template("changedOrganizerPassScreen.html")

@app.route('/notValidPass', methods = ['GET', 'POST'])
def notValidPass():
    return render_template("notValidPassScreen.html")

@app.route('/passwordsDontMatch', methods = ['GET', 'POST'])
def passwordsDontMatch():
    return render_template("passwordsDontMatch.html")

#main method
if __name__ == '__main__':
    app.run(debug = True)
