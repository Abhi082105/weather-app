import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = []
    labels = []
    temps = []
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if not API_KEY:
            error = "API key not set!"
            return render_template("index.html", weather=None, forecast=[], labels=[], temps=[], error=error)

        # Current weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        weather_res = requests.get(weather_url).json()

        if weather_res.get("cod") != 200:
            error = weather_res.get("message", "Error fetching weather")
            return render_template("index.html", weather=None, forecast=[], labels=[], temps=[], error=error)

        weather = {
            "city": weather_res["name"],
            "temp": weather_res["main"]["temp"],
            "humidity": weather_res["main"]["humidity"],
            "desc": weather_res["weather"][0]["description"]
        }

        # Forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_res = requests.get(forecast_url).json()

        if forecast_res.get("cod") == "200":
            for item in forecast_res["list"][:8]:
                time = item["dt_txt"]
                temp = item["main"]["temp"]

                labels.append(time.split()[1][:5])
                temps.append(temp)

                forecast.append({
                    "time": time,
                    "temp": temp
                })

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        labels=labels,
        temps=temps,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
