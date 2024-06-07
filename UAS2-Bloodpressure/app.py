from flask import Flask, render_template, request
from joblib import load

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/registration-form', methods=['POST', 'GET'])
def registration_form():
    nama = request.form.get('nama', '')  # Use get method to avoid KeyError
    return render_template('forms.html', nama=nama)

def calculate_limit(klaim):
    if klaim < 1000:
        return klaim * 0.25
    elif 1000 < klaim < 3000:
        return klaim * 0.41
    elif 3000 < klaim < 5000:
        return klaim * 0.35
    elif 5000 < klaim < 10000:
        return klaim * 0.32
    else:
        return klaim * 0.5

def calculate_biaya(klaim):
    if klaim < 1000:
        return klaim * 0.0025
    elif 1000 < klaim < 3000:
        return klaim * 0.0029
    elif 3000 < klaim < 5000:
        return klaim * 0.00275
    elif 5000 < klaim < 10000:
        return klaim * 0.003
    else:
        return klaim * 0.004
    
    
@app.route('/result', methods=['POST','GET'])
def result():

    try:
        age = float(request.form['age'])
        sex = int(request.form['sex'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = weight / (height**2)
        hereditary_diseases = int(request.form['hereditary_diseases'])
        no_of_dependents = int(request.form['no_of_dependents'])
        smoker = int(request.form['smoker'])
        city = int(request.form['city'])
        diabetes = int(request.form['diabetes'])
        regular_ex = int(request.form['regular_ex'])
        job_title = int(request.form['job_title'])

        print(request.form)

        model = load('model_rf.joblib')

        # Make predictions 
        prediction = model.predict([[age, sex, weight, bmi, hereditary_diseases, no_of_dependents, smoker, city, diabetes, regular_ex, job_title]])

        global klaim
        klaim = prediction[0] 

        result = f"The predicted result is: ${round(klaim, 2)}"

        limit = round(calculate_limit(klaim), 2)
        biaya = round(calculate_biaya(klaim), 2)

        return render_template('result.html', result=result, limit=limit, biaya=biaya)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template('result.html', error_message="An error occurred. Please try again.")

def form():
    premi = None  # Default result value
    if request.method == 'POST':
        jumlah_tahun_str = request.form.get('lamaTahunSelect')
        if jumlah_tahun_str is not None:
            try:
                jumlah_tahun = int(jumlah_tahun_str)
                premi = calculate_premi(jumlah_tahun)
            except ValueError as e:
                print(f"Error converting 'lamaTahunSelect' to an integer: {e}")

    return render_template('result.html', premi=premi)


def calculate_premi(jumlah_tahun):
    try:
        premi = klaim / (jumlah_tahun * 12) + ((klaim / (jumlah_tahun * 12)) * 3.6 / (jumlah_tahun * 12))
        premi = round(premi, 2)
        return premi
    except Exception as e:
        print(f"An error occurred in calculate_premi: {str(e)}")
        return None


@app.route('/analytics', methods=['POST'])
def analytics():
    nama = request.form.get('nama', '')  # Use get method to avoid KeyError
    return render_template('analytics.html', nama=nama)

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/calculate-premi', methods=['POST'])
# def calculate_premi_route():
#     try:
#         jumlah_tahun = int(request.form['jumlah_tahun'])

#         premi = calculate_premi(klaim, jumlah_tahun)

#         return render_template('premi.html', premi=premi)

#     except Exception as e:
#         print(f"An error occurred in calculate_premi_route: {str(e)}")
#         return render_template('premi.html', error_message="An error occurred. Please try again.")



