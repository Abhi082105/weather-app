import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

# 🔍 City suggestions (simple static list)
CITIES = ["London", "New York", "Delhi", "Tokyo", "Paris", "Mumbai", "Sydney"]

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
            error = "API key missing"
            return render_template("index.html", error=error)

        # 🌤 Current weather
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") != 200:
            error = res.get("message")
            return render_template("index.html", error=error)

        weather = {
            "city": res["name"],
            "temp": res["main"]["temp"],
            "humidity": res["main"]["humidity"],
            "desc": res["weather"][0]["description"]
        }

        # 📊 Forecast
        f_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        f_res = requests.get(f_url).json()

        if f_res.get("cod") == "200":
            for item in f_res["list"][:8]:
                time = item["dt_txt"].split()[1][:5]
                temp = item["main"]["temp"]

                labels.append(time)
                temps.append(temp)

                forecast.append({
                    "time": time,
                    "temp": temp
                })

    return render_template("index.html",
                           weather=weather,
                           forecast=forecast,
                           labels=labels,
                           temps=temps,
                           error=error,
                           cities=CITIES)

# 📍 Auto location API
@app.route("/weather_by_coords")
def weather_by_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()

    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
