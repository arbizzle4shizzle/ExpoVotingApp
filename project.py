from flask import Flask
from flask import render_template
import csv
app = Flask(__name__)

@app.route('/')
def hello_world():
	with open("data/votes.csv",'rb') as readFile:
		votes_table = []
		reader = csv.reader(readFile)
		for row in reader:
			votes_table.append(row)
    	return render_template('results.html',votes_table=votes_table)