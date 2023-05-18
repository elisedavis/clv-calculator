from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def clvInputs():
    return render_template('Calculator.html')

if __name__ == '__main__': 
    app.run(debug=True)

@app.route("/results")
def clvResults():
    return "<h1>CLV Calculation Results</h1>"