from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #36d1dc, #5b86e5);
        }

        .card {
            width: 90%;
            max-width: 420px;
            padding: 30px;
            text-align: center;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px #0003;
        }

        h1 {
            color: #2457a7;
            margin-top: 0;
        }

        input {
            width: 100%;
            padding: 13px;
            margin: 12px 0;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 13px;
            color: white;
            background: #2457a7;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #173d79;
        }

        .weather {
            margin-top: 22px;
            padding: 18px;
            background: #eef6ff;
            border-radius: 12px;
        }

        .temp {
            font-size: 42px;
            font-weight: bold;
            color: #2457a7;
        }

        .error {
            color: #c62828;
            margin-top: 15px;
        }

        .small {
            color: #666;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌤 Weather App</h1>
        <p>Check the current weather in your city</p>

        <form method="POST">
            <input
                type="text"
                name="city"
                placeholder="Enter city (e.g. Vellore)"
                value="{{ city }}"
                required
            >
            <button type="submit">Get Weather</button>
        </form>

        {% if weather %}
        <div class="weather">
            <h2>{{ weather.city }}</h2>
            <div class="temp">{{ weather.temperature }}°C</div>
            <p>{{ weather.description }}</p>
            <p>💨 Wind speed: {{ weather.wind }} km/h</p>
            <p>🌡 Feels like: {{ weather.temperature }}°C</p>
        </div>
        {% endif %}

        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}

        <p class="small">Weather data: Open-Meteo</p>
    </div>
</body>
</html>
"""

def get_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm"
    }
    return descriptions.get(code, "Weather conditions unavailable")


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        try:
            # Find the city coordinates
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_response = requests.get(
                geo_url,
                params={"name": city, "count": 1, "language": "en"},
                timeout=10
            )
            geo_response.raise_for_status()
            locations = geo_response.json().get("results", [])

            if not locations:
                error = "City not found. Please check the spelling."
            else:
                place = locations[0]
                latitude = place["latitude"]
                longitude = place["longitude"]

                # Get current weather
                weather_url = "https://api.open-meteo.com/v1/forecast"
                response = requests.get(
                    weather_url,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": (
                            "temperature_2m,"
                            "relative_humidity_2m,"
                            "apparent_temperature,"
                            "wind_speed_10m,"
                            "weather_code"
                        )
                    },
                    timeout=10
                )
                response.raise_for_status()
                current = response.json()["current"]

                weather = {
                    "city": place["name"],
                    "temperature": current["temperature_2m"],
                    "description": get_description(
                        current["weather_code"]
                    ),
                    "wind": current["wind_speed_10m"]
                }

        except requests.RequestException:
            error = "Unable to connect to the weather service. Try again."
        except (KeyError, ValueError, IndexError):
            error = "Unable to read weather data. Please try again."

    return render_template_string(
        HTML, city=city, weather=weather, error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
