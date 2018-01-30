from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def welcomeScreen():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def voting():
	print('In vote.py')
	return render_template('results.html')

if __name__ == '__main__':
    app.run(debug = True)