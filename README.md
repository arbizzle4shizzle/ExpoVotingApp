# ExpoVotingApp
A web application that allows expo visitors to vote on their favorite Junior Design project.

## Running the Flask Application

To run the flask app, open the command promt and navigate to the folder that holds the full application. Ensure that you have virtualenv installed on your computer using [these instructions](http://flask.pocoo.org/docs/0.11/installation/#installation).

If you don't have a venv/ folder in the project directory, run the following command:

    $ virtualenv venv

In the command line, enter the following code to activate the virtual environment:

__**Mac/Linux:**__

    $ venv/bin/activate
   
__**Windows:**__

    $ venv\scripts\activate

Now, enter the following code to run the flask app:

__**Mac/Linux:**__
   
    $ export FLASK_APP=main.py
    $ flask run
        * Running on http://127.0.0.1:5000/
        
__**Windows:**__

    $ set FLASK_APP=main.py
    $ flask run
        * Running on http://127.0.0.1:5000/

Now, just head over to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the running application.
