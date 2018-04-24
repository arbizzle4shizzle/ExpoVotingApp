# ExpoVotingApp
A web application that allows expo visitors to vote on their favorite Junior Design project.

# Release Notes

## Version 1.0

### Features
The expo voting app supports the following roles and role-specific functionalities:
#### Attendee
* Cast one vote on a team's project
* Search for a specific team or project
* Leave comments for a team
#### Organizer
* View voting results
* Upload .csv file of projects
* View comments left for teams
* Send comments to teams
* Delete inappropriate comments
#### Administrator
* Change attendee password
* Change organizer password

## Defects and Future Work (in order of descending importance)
1. The app’s database is currently hosted on www.freemysqlhosting.net, however, this site requires a biweekly renewal to utilize the free storage. The database should be hosted on a local SQL server. 

2. When running the Flask app on the jrdesign.cc.gatech.edu virtual machine during the expo, the app crashed unexpectedly. The cause could not be diagnosed, but the issue was fixed by signing into a different account on the virtual machine and running the website from a different account.

3. The map of the Klaus Atrium was not incorporated in our application; adding an interactive floor map would help clients and other attendees find specific teams by their location and discover information about teams at the expo.

4. Currently, the application can only be accessed by attendees on Georgia Tech wireless connections. If possible, anyone should be able to access the app as visiting clients may not have access to Georgia Tech internet networks. Server Help Email: helpdesk@cc.gatech.edu.

5. Another feature to implement is a pop-up or separate page to confirm a user’s voting choice. Currently, after selecting “Vote,” the vote will be counted, and the user will no longer be able to submit any votes.

6. A feature we didn’t have enough time to implement was to support separate voting for the multiple sessions throughout the day. Ideally, users would only be shown the session 1 projects during session 1 and likewise with session 2. Additionally, the same user should be able to vote once in each session.

7. In conjunction with the previous feature, the results viewing should separate the teams between session 1 and 2 so that a winner from each session can be selected.

# Install Guide

## Pre-requesites:
* Python 2.7
* Pip
* Git
## Dependent Libraries that must be installed:
* Flask
* Flask-MySQL
## Download Instructions
To run the application, you must clone this repository to your computer. To do so, run the following command in a command prompt
    
    $ git clone https://github.com/arbermuharemi/ExpoVotingApp.git 
    
## Running the Flask Application

To run the flask app, open the command prompt and navigate to the folder that holds the full application. Ensure that you have virtualenv installed on your computer using [these instructions](http://flask.pocoo.org/docs/0.11/installation/#installation).

If you don't have a venv/ folder in the project directory, run the following command:

    $ virtualenv venv

### Installing packages
Be sure you have the proper packages on the virutal environment to run the app.  These include flask, flask-mysql, and Flask-Mail

 	$pip install flask
 	$pip install flask-mysql
 	$pip install Flask-Mail
 	
### Testing/Development (Local)
In the command line, enter the following lines to activate the virtual environment and run the flask app:

**__change main.py to the file name of the file where the program starts__**

__**Mac/Linux:**__

    $ . venv/bin/activate
    $ export FLASK_APP=main.py
    $ flask run
        * Running on http://127.0.0.1:5000/
        
__**Windows:**__

    $ venv\scripts\activate
    $ set FLASK_APP=main.py
    $ flask run
        * Running on http://127.0.0.1:5000/

Now, just head over to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the locally running application.

### Running the Site (Public)
1. Connect to the school VPN following [this instructions](https://faq.oit.gatech.edu/content/how-do-i-get-started-campus-vpn)
2. Connect to __jrdesign.cc.gatech.edu__ (the virtual machine) via Windows Remote Connection using your GT username @ gatech.edu (eg: amuharemi3@gatech.edu) and GT password to login.
3. If the ExpoVotingApp directory doesn't exist, clone this repository to a directory on the virutal machine

In the command line in the __jrdesign.cc.gatech.edu__ desktop, enter the following lines to activate the virtual environment and run the flask app:

**__change main.py to the file name of the file where the program starts__**

    $ venv\scripts\activate
    $ set FLASK_APP=main.py
    $ flask run --host=0.0.0.0 --port=80
        * Running on http://0.0.0.0:80/

Now, navigate to [http://jrdesign.cc.gatech.edu/](http://jrdesign.cc.gatech.edu/) to view the running application.

## Database
To view and edit the database, use the following information below

### Development Database Info:
* Website: [http://www.phpmyadmin.co/](http://www.phpmyadmin.co/)
* Server/Host: sql9.freemysqlhosting.net
* Name: sql9219692
* Username: sql9219692
* Password: 5M2YS1HZdZ
* Port Number: 3306
