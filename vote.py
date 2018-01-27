from flask import Flask


vote = Flask(__name__)

@vote.route('/')

def voting():

	return 'This is where the projects to be voted on will be displayed'

if __name__ == '__main__':
	vote.run()