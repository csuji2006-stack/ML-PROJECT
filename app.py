from flask import Flask, render_template, request, jsonify, send_from_directory
# import joblib
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load models (run main.py first to generate them)
# scaler = joblib.load('scaler.pkl')
# log_reg = joblib.load('irr_classifier.pkl')
# lin_reg = joblib.load('water_regressor.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    
    soil = float(data['soil_moisture'])
    temp = float(data['temperature'])
    hum = float(data['humidity'])
    rain = float(data['rainfall_hist'])
    
    input_data = np.array([[soil, temp, hum, rain]])
    # input_scaled = scaler.transform(input_data)
    
    # Dummy prediction logic for testing
    irr_req = "Yes" if soil < 50 and temp > 25 else "No"
    water_liters = round((100 - soil) * 0.5 + temp * 0.1, 2)
    
    # Generate chart
    labels = ['Soil Moisture', 'Temperature', 'Humidity', 'Rainfall']
    values = [soil, temp, hum, rain]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['brown', 'red', 'blue', 'gray'])
    plt.title('Sensor Data Input')
    plt.ylabel('Values')
    plt.ylim(0, 100)
    chart_path = os.path.join('static', 'images', 'chart.png')
    plt.savefig(chart_path)
    plt.close()
    
    if request.is_json:
        return jsonify({'irrigation': irr_req, 'water_qty': water_liters})
    else:
        return render_template('index.html', 
                             irr_req=irr_req, 
                             water_qty=water_liters,
                             soil_moisture=soil,
                             temperature=temp,
                             humidity=hum,
                             rainfall_hist=rain,
                             chart_path='/static/images/chart.png')

if __name__ == '__main__':
    app.run(debug=True)