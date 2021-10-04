from flask import Flask, escape, request, render_template
import pickle
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

model = pickle.load(open("model_pickle.pkl", 'rb'))

app = Flask(__name__)
@app.route('/analysis')
def analysis():
    return render_template("stroke.html")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method =="POST":
        gender = request.form['gender']
        age = int(request.form['age'])
        hypertension = int(request.form['hypertension'])
        disease = int(request.form['heart_disease'])
        married = request.form['married']
        work = request.form['work']
        residence = request.form['residence']
        glucose = float(request.form['glucose'])
        bmi = float(request.form['bmi'])
        smoking = request.form['smoking']

        # gender
        if (gender == "Male"):
            gender=1.0
        elif(gender == "Female"):
            gender=0.0
        else:
            gender=2.0
        
        # married
        if(married=="Yes"):
            ever_married = 1
        else:
            ever_married=0

        # work  type
        if(work=='Self-employed'):
            work_type= 3.0
        elif(work == 'Private'):
            work_type= 2.0
        elif(work =="children"):
            work_type= 0.0
        elif(work =="Never_worked"):
            work_type=1.0
        else:
            work_type=4.0

        # residence type
        if (residence=="Urban"):
            Residence_type=1.0
        else:
            Residence_type=0.0

        # smoking sttaus
        if(smoking=='formerly smoked'):
            smoking_status = 1.0
        elif(smoking == 'smoked'):
            smoking_status = 3.0
        elif(smoking=="never smoked"):
            smoking_status=2.0
        else:
            smoking_status=0.0

        feature = scaler.fit_transform([[age, hypertension, disease, glucose, bmi, gender, ever_married, work_type, Residence_type, smoking_status]])

        prediction = model.predict(feature)[0]
        # print(prediction) 
        # 
        if prediction==0:
            prediction = "NO" 
        else:
            prediction = "YES" 

        return render_template("index.html", prediction_text="Chance of Stroke Prediction is --> {}".format(prediction))   
         

    else:
        return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)