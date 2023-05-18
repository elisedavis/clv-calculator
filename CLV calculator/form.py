from flask import Flask, render_template, flash
from forms import clvData
from calc import calculate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

user_data = {
    'user_percentile': '',
    'api_key': '',
    'email': ''  
}
api_response = ''

@app.route("/", methods=['GET','POST'])
def clvInputs():
    form = clvData()
    # if form.validate_on_submit():
    #     apiKey = form.data.get('apiKey')
    #     email = form.data.get('email')
    #     percentile = form.data.get('clvThreshold')
    #     flash("Success! We'll email you the results")
    #     calculate(apiKey,email,percentile)
    return render_template('Calculator.html', user_data=user_data, form=form)

@app.route("/confirmation", methods=['GET','POST'])
def clvOutputs():
    form = clvData()
    if form.validate_on_submit():
        apiKey = form.data.get('apiKey')
        email = form.data.get('email')
        percentile = form.data.get('clvThreshold')
        flash("Success! We'll email you the results")
        calculate(apiKey,email,percentile)
    return render_template('Calculator_results.html', user_data=user_data)


if __name__ == '__main__': 
    app.run(debug=True)

