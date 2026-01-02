from flask import Flask, request, Response
app = Flask(_name_)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        soil = float(request.form['soil'])
        temp = float(request.form['temp'])
        hum = float(request.form['hum'])
        rain = float(request.form['rain'])
        
        # ML CALCULATION
        irr_req = "Yes" if (soil < 30 or temp > 35 or rain < 5) else "No"
        water = round(max(0, (30-soil)*1.5 + (temp-30)*0.5
