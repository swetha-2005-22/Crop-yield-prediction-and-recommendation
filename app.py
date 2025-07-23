from flask import Flask, render_template, request
import pickle
import numpy as np

model1 = pickle.load(open(r"C:\Users\DELL\OneDrive\Desktop\crop\model\agriculture.pkl",'rb'))  

app = Flask(__name__)  # initializing Flask app


@app.route("/",methods=['GET'])
def hello():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST': 
        d1 = request.form['N']
        d2 = request.form['P']
        d3 = request.form['K']
        d4 = request.form['temperature']
        d5 = request.form['humidity']
        d6 = request.form['ph']
        d7 = request.form['rainfall']
        
        

        arr = np.array([[d1,d2,d3,d4,d5,d6,d7]])
        print([d1,d2,d3,d4,d5,d6,d7])
        pred1 = model1.predict(arr)
        print(pred1)

    return render_template('result.html',prediction_text1=pred1)
    
if __name__ == '__main__':
    app.run(debug=True)
    
#app.run(host="0.0.0.0")            # deploy
            # run on local system
