from flask import Flask, request, jsonify, send_from_directory

app = Flask(_name_, static_folder='static', static_url_path='')

# Serve static files (HTML, CSS, JS)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    data = request.get_json()
    soil = float(data.get('soil', 0))
    temp = float(data.get('temp', 0))
    hum = float(data.get('hum', 0))
    rain = float(data.get('rain', 0))
    
    # ML CALCULATION
    irr_req = "Yes" if (soil < 30 or temp > 35 or rain < 5) else "No"
    water_qty = round(max(0, (30-soil)*1.5 + (temp-30)*0.5 - rain*0.8), 1)
    
    # JSON Response (like StackOverflow example)
    response = {
        "irr_req": irr_req,
        "water_qty": water_qty,
        "soil": soil,
        "temp": temp,
        "hum": hum,
        "rain": rain,
        "status": "success"
    }
    
    return jsonify(response)

if _name_ == '_main_':
    print("🚀 Server running at http://127.0.0.1:5000")
    print("📁 Put index.html in 'static' folder")
    app.run(debug=True, port=5000)
