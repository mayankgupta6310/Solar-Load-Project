# ☀️ Solar Load Project

A Flask-based web app that estimates solar power generation for any location using real-world solar irradiance and weather data.

Enter a latitude/longitude and the app shows expected daily and monthly solar generation, current output, estimated cost savings and a 7-day forecast.

## Features

- Fetches solar irradiance data from the **NASA POWER API**
- Fetches live temperature and cloud cover from the **OpenWeather API**
- Adjusts solar output based on cloud cover
- Estimates **daily generation, monthly generation and cost savings** (₹)
- Estimates **current (right now) power output** based on time of day
- Generates a **7-day generation forecast**
- Simple web dashboard (HTML frontend)

## Tech Stack

- **Backend:** Python, Flask
- **Data processing:** Pandas, NumPy
- **APIs:** NASA POWER, OpenWeatherMap
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
Solar-Load-Project/
├── app.py                            # Flask app and API routes
├── templates/                        # HTML templates (index.html)
├── requirements.txt                  # Python dependencies
├── test_api.py                       # API testing script
├── Solar_Api_Integration.ipynb       # Notebook for API experiments
└── OpenWeather and Nasa Api Intgration.txt   # API integration notes
```

## Installation

1. Clone the repository
```bash
   git clone https://github.com/mayankgupta6310/Solar-Load-Project.git
   cd Solar-Load-Project
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Set your OpenWeather API key (get a free one from [openweathermap.org](https://openweathermap.org/api))

   Windows:
```bash
   set OPENWEATHER_API_KEY=your_api_key_here
```
   Linux / macOS:
```bash
   export OPENWEATHER_API_KEY=your_api_key_here
```

4. Run the app
```bash
   python app.py
```

5. Open `http://127.0.0.1:5000` in your browser.

## API Endpoint

`GET /api/solar?lat=<latitude>&lon=<longitude>`

Example: `/api/solar?lat=26.85&lon=80.95`

Sample response:
```json
{
  "irradiance": 5.2,
  "temp": 31.4,
  "clouds": 20,
  "daily_gen": 6.65,
  "current_output": 1.1,
  "monthly_gen": 206.15,
  "cost_saving": 1236.9,
  "prediction": [6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9]
}
```

## How It Works

1. Average solar irradiance (kWh/m²/day) is fetched from NASA POWER for the given coordinates.
2. Current temperature and cloud cover are fetched from OpenWeather.
3. Irradiance is reduced according to cloud cover.
4. Daily generation = adjusted irradiance × system size (default **1.6 kW**).
5. Monthly generation and savings are calculated assuming **₹6 per kWh**.
6. A 7-day forecast is produced from the daily estimate with a small variation.

## Configuration

- System size (1.6 kW) and electricity rate (₹6/kWh) can be changed in `app.py`.

## Future Improvements

- Let users choose system size and electricity tariff from the UI
- Use a real ML model for forecasting instead of trend + noise
- Add charts for generation history
- Deploy online (Render / Railway)

## Author

**Mayank Gupta** — [@mayankgupta6310](https://github.com/mayankgupta6310)
