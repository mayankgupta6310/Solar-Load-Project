from flask import Flask, jsonify, render_template, request
import os
import requests
import pandas as pd
import numpy as np
import datetime

app = Flask(__name__)

# ---------- NASA API Function ----------
def get_nasa_data(lat, lon):
    """Fetch solar irradiance data from NASA POWER API."""
    try:
        lat = round(float(lat), 2)
        lon = round(float(lon), 2)
        start_year = 2023
        end_year = 2024

        nasa_url = (
            f"https://power.larc.nasa.gov/api/temporal/monthly/point?"
            f"parameters=ALLSKY_SFC_SW_DWN&start={start_year}&end={end_year}"
            f"&latitude={lat}&longitude={lon}&community=RE&format=JSON"
        )

        response = requests.get(nasa_url)
        data = response.json()
        irradiance_data = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]

        df = pd.DataFrame(irradiance_data.items(), columns=["month", "irradiance_kWh_m2_day"])
        df = df[df["irradiance_kWh_m2_day"] > 0]

        avg_irradiance = df["irradiance_kWh_m2_day"].mean()
        return avg_irradiance

    except Exception as e:
        print(f"❌ Error parsing NASA data: {e}")
        return 4.5

# ---------- OpenWeather Function ----------
def get_weather_data(lat, lon):
    """Fetch current temperature and cloud cover."""
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        res = requests.get(url)
        data = res.json()
        temp = data["main"]["temp"]
        clouds = data["clouds"]["all"]
        return temp, clouds
    except Exception as e:
        print(f"❌ Weather data error: {e}")
        return 25.0, 10

# ---------- Flask Routes ----------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/solar')
def get_solar_data():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))

        irradiance = get_nasa_data(lat, lon)
        temp, clouds = get_weather_data(lat, lon)

        # Calculations
        efficiency = (100 - (clouds * 0.5)) / 100
        adjusted_irradiance = irradiance * efficiency
        daily_generation = adjusted_irradiance * 1.6  # 1.6kW System size
        monthly_generation = daily_generation * 31
        cost_saving = monthly_generation * 6

        # --- NEW: Current Instantaneous Power Prediction ---
        # estimating "Right Now" based on time of day (Gaussian curve simulation)
        hour = datetime.datetime.now().hour
        if 6 <= hour <= 18:
            # Peak at noon (12), zero at 6am/6pm
            peak_factor = np.exp(-0.1 * (hour - 12)**2)
            current_output = (daily_generation / 5) * peak_factor # Approx kW right now
        else:
            current_output = 0.0

        # Prediction Array (Next 7 days)
        trend = np.linspace(daily_generation * 0.95, daily_generation * 1.05, 7)
        noise = np.random.uniform(-0.1, 0.1, 7)
        prediction = (trend * (1 + noise)).round(2).tolist()

        return jsonify({
            "irradiance": round(irradiance, 2),
            "temp": round(temp, 1),
            "clouds": clouds,
            "daily_gen": round(daily_generation, 2),
            "current_output": round(current_output, 2), # <--- NEW FIELD
            "monthly_gen": round(monthly_generation, 2),
            "cost_saving": round(cost_saving, 2),
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)