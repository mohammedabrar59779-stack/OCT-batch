
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# HTML and CSS in the same Python file
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #36d1dc, #5b86e5);
            padding: 20px;
        }

        .card {
            width: 100%;
            max-width: 430px;
            padding: 30px;
            background: white;
            border-radius: 22px;
            text-align: center;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
        }

        h1 {
            color: #2457a7;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 25px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
            margin-bottom: 12px;
        }

        input:focus {
            border-color: #2457a7;
        }

        button {
            width: 100%;
            padding: 14px;
            background: #2457a7;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #173d79;
        }

        .weather {
            margin-top: 25px;
            padding: 20px;
            background: #eef6ff;
            border-radius: 15px;
        }

        .weather-icon {
            font-size: 50px;
        }

        .temperature {
            font-size: 48px;
            font-weight: bold;
            color: #2457a7;
            margin: 10px 0;
        }

        .condition {
            font-size: 19px;
            color: #333;
        }

        .details {
            display: flex;
            justify-content: space-around;
            gap: 10px;
            margin-top: 20px;
        }

        .detail {
            flex: 1;
            padding: 12px 5px;
            background: white;
            border-radius: 10px;
            font-size: 14px;
        }

        .detail strong {
            display: block;
            margin-top: 8px;
            color: #2457a7;
            font-size: 17px;
        }

        .error {
            color: #c62828;
            margin-top: 18px;
        }

        .footer {
            font-size: 12px;
            color: #777;
            margin-top: 20px;
        }
    </style>
</head>

<body>
    <div class="card">
        <h1>🌤 Weather App</h1>
        <p class="subtitle">Check the weather in any city</p>

        <form method="POST">
            <input
                type="text"
                name="city"
                placeholder="Enter city name, e.g. Vellore"
                value="{{ city }}"
                required
            >
            <button type="submit">Search Weather</button>
        </form>

        {% if weather %}
        <div class="weather">
            <div class="weather-icon">{{ weather.icon }}</div>
            <h2>{{ weather.city }}</h2>

            <div class="temperature">
                {{ weather.temperature }}°C
            </div>

            <p class="condition">{{ weather.description }}</p>

            <div class="details">
                <div class="detail">
                    💨 Wind
                    <strong>{{ weather.wind }} km/h</strong>
                </div>

                <div class="detail">
                    💧 Humidity
                    <strong>{{ weather.humidity }}%</strong>
                </div>
            </div>
        </div>
        {% endif %}

        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}

        <p class="footer">
            Weather data provided by Open-Meteo
        </p>
    </div>
</body>
</html>
"""


def get_weather_info(code):
    weather_codes = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Rime fog", "🌫️"),
        51: ("Light drizzle", "🌦️"),
        53: ("Moderate drizzle", "🌦️"),
        55: ("Heavy drizzle", "🌧️"),
        61: ("Slight rain", "🌧️"),
        63: ("Moderate rain", "🌧️"),
        65: ("Heavy rain", "🌧️"),
        71: ("Slight snow", "🌨️"),
        73: ("Moderate snow", "❄️"),
        75: ("Heavy snow", "❄️"),
        80: ("Rain showers", "🌦️"),
        81: ("Moderate rain showers", "🌧️"),
        82: ("Heavy rain showers", "⛈️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with hail", "⛈️"),
        99: ("Severe thunderstorm with hail", "⛈️")
    }

    return weather_codes.get(code, ("Conditions unavailable", "🌡️"))


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        else:
            try:
                # Step 1: Find the city coordinates
                geo_url = "https://geocoding-api.open-meteo.com/v1/search"

                geo_response = requests.get(
                    geo_url,
                    params={
                        "name": city,
                        "count": 1,
                        "language": "en",
                        "format": "json"
                    },
                    timeout=10
                )
                geo_response.raise_for_status()

                locations = geo_response.json().get("results", [])

                if not locations:
                    error = "City not found. Check the spelling and try again."
                else:
                    place = locations[0]
                    latitude = place["latitude"]
                    longitude = place["longitude"]

                    # Step 2: Get current weather
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
                            ),
                            "timezone": "auto"
                        },
                        timeout=10
                    )
                    response.raise_for_status()

                    current = response.json()["current"]

                    description, icon = get_weather_info(
                        current["weather_code"]
                    )

                    weather = {
                        "city": place["name"],
                        "temperature": current["temperature_2m"],
                        "description": description,
                        "icon": icon,
                        "wind": current["wind_speed_10m"],
                        "humidity": current["relative_humidity_2m"]
                    }

            except requests.RequestException:
                error = (
                    "Could not connect to the weather service. "
                    "Check your internet connection and try again."
                )
            except (KeyError, ValueError, IndexError, TypeError):
                error = "Weather data is unavailable. Please try again."

    return render_template_string(
        HTML,
        city=city,
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
