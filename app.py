from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b6e6b8452d8045cc4386ee0d2c914b9e"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = []
    dates = []
    temps = []
    bg = "default"

    if request.method == "POST":
        city = request.form.get("city")
        lat = request.form.get("lat")
        lon = request.form.get("lon")

        # 📍 Choose API based on input
        if lat and lon:
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        else:
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        weather_json = requests.get(weather_url).json()
        forecast_json = requests.get(forecast_url).json()

        if weather_json.get("cod") == 200:

            description = weather_json["weather"][0]["description"]

            # 🌈 Background logic
            if "clear" in description:
                bg = "sunny"
            elif "cloud" in description:
                bg = "cloudy"
            elif "rain" in description:
                bg = "rainy"

            weather_data = {
                "city": weather_json["name"],
                "temp": weather_json["main"]["temp"],
                "feels_like": weather_json["main"]["feels_like"],
                "humidity": weather_json["main"]["humidity"],
                "description": description,
                "icon": weather_json["weather"][0]["icon"]
            }

            # 📅 Forecast + chart data
            for i in range(0, len(forecast_json["list"]), 8):
                item = forecast_json["list"][i]

                date = item["dt_txt"].split(" ")[0]
                temp = item["main"]["temp"]

                dates.append(date)
                temps.append(temp)

                forecast_data.append({
                    "date": date,
                    "temp": temp,
                    "icon": item["weather"][0]["icon"]
                })

        else:
            weather_data = {"error": weather_json.get("message")}

    return render_template(
        "index.html",
        weather=weather_data,
        forecast=forecast_data,
        bg=bg,
        dates=dates,
        temps=temps
    )


if __name__ == "__main__":
    app.run(debug=True)