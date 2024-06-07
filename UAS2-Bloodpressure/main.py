from flask import Flask, render_template, request
from joblib import load, dump

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("home.html")

@app.route('/registration-form')
def registration_form():
    return render_template('register.html')

@app.route('/analytics', methods=['POST'])
def analytics():
    nama = request.form['nama']
    return render_template('analytics.html', nama=nama)

@app.route('/result', methods=['POST'])
def result():
    # Retrieve form data
    age = float(request.form['age'])
    sex = int(request.form['sex'])
    weight = float(request.form['weight'])
    bmi = float(request.form['bmi'])
    hereditary_diseases = int(request.form['hereditary'])
    no_of_dependents = int(request.form['depends'])
    smoker = int(request.form['smoker'])
    city = int(request.form['city'])
    bloodpressure = float(request.form['bloodpressure'])
    diabetes = int(request.form['diabet'])
    regular_ex = int(request.form['regular'])
    job_title = int(request.form['job'])

    # Preprocess the input data if needed
    model = load('model.joblib')

    # Make predictions using the loaded model
    prediction = model.predict([[age, sex, weight, bmi, hereditary_diseases, no_of_dependents, smoker, city, bloodpressure, diabetes, regular_ex, job_title]])

    # You can format the prediction or use it as needed
    result = f"The predicted result is: ${prediction[0]}"

    # Return the result to the user
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
