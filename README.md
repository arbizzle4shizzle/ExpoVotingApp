# ExpoVotingApp
A web application that allows expo visitors to vote on their favorite Junior Design project.

## Running the Flask Application

To run the flask app, open the command promt and navigate to the folder that holds the full application. Ensure that you have virtualenv installed on your computer using [these instructions](http://flask.pocoo.org/docs/0.11/installation/#installation).

In the command line, enter the following code to activate the virtual environment:

    $ venv\scripts\activate

If you're using a Mac, you'll need to use the following code:

    $ venv/bin/activate

Now, enter the following code to run the flask app:

__**Windows:**__

    $ set FLASK_APP=main.py
    $ flask run
        * Running on http://127.0.0.1:5000/
        
__**Mac/Linux:**__

    $ export FLASK_APP=main.py
    $ flask run
        * Running on http://127.0.0.1:5000/

Now, just head over to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the running application.
