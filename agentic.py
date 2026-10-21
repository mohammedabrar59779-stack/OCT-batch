"""
weather.py — Get a current weather report for any city.

Uses the free Open-Meteo geocoding and forecast APIs.
No API key or third-party Python package is required.

Run:
    python weather.py
"""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def get_json(url):
    """Fetch JSON from an API endpoint."""
    request = Request(
        url,
        headers={"User-Agent": "BeginnerWeatherApp/1.0"}
    )
    with urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_city_coordinates(city):
    """Find a city's latitude, longitude, and country."""
    query = urlencode({
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    })
    data = get_json(f"https://geocoding-api.open-meteo.com/v1/search?{query}")
    results = data.get("results", [])

    if not results:
        return None

    place = results[0]
    return {
        "name": place["name"],
        "country": place.get("country", "Unknown"),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "timezone": place.get("timezone", "auto"),
    }


def describe_weather(code):
    """Convert a WMO weather code into a readable description."""
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return descriptions.get(code, "Unknown conditions")


def show_weather(city):
    """Print the current weather for the requested city."""
    place = get_city_coordinates(city)

    if place is None:
        print(f"Could not find '{city}'. Check the spelling and try again.")
        return

    query = urlencode({
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "is_day,precipitation,rain,showers,snowfall,weather_code,"
            "wind_speed_10m"
        ),
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset",
        "timezone": place["timezone"],
        "forecast_days": 1,
    })
    data = get_json(f"https://api.open-meteo.com/v1/forecast?{query}")
    current = data.get("current", {})
    units = data.get("current_units", {})
    daily = data.get("daily", {})

    print("\n" + "=" * 38)
    print(f" WEATHER REPORT: {place['name']}, {place['country']}")
    print("=" * 38)
    print(f"Local time:       {current.get('time', 'N/A').replace('T', ' ')}")
    print(
        f"Condition:        "
        f"{describe_weather(current.get('weather_code', -1))}"
    )
    print(
        f"Temperature:      {current.get('temperature_2m', 'N/A')} "
        f"{units.get('temperature_2m', '°C')}"
    )
    print(
        f"Feels like:       {current.get('apparent_temperature', 'N/A')} "
        f"{units.get('apparent_temperature', '°C')}"
    )
    print(
        f"Humidity:         {current.get('relative_humidity_2m', 'N/A')}"
        f"{units.get('relative_humidity_2m', '%')}"
    )
    print(
        f"Wind speed:       {current.get('wind_speed_10m', 'N/A')} "
        f"{units.get('wind_speed_10m', 'km/h')}"
    )
    print(f"Precipitation:    {current.get('precipitation', 'N/A')} mm")
    print(f"Rain:             {current.get('rain', 'N/A')} mm")
    print(f"Showers:          {current.get('showers', 'N/A')} mm")
    print(f"Snowfall:         {current.get('snowfall', 'N/A')} cm")

    if daily.get("temperature_2m_max"):
        print(
            f"Today's high:     {daily['temperature_2m_max'][0]} "
            f"{data.get('daily_units', {}).get('temperature_2m_max', '°C')}"
        )
        print(
            f"Today's low:      {daily['temperature_2m_min'][0]} "
            f"{data.get('daily_units', {}).get('temperature_2m_min', '°C')}"
        )
        print(f"Sunrise:          {daily.get('sunrise', ['N/A'])[0]}")
        print(f"Sunset:           {daily.get('sunset', ['N/A'])[0]}")

    print("=" * 38)
    print("Data source: Open-Meteo (free API)")


def main():
    print("🌦️  City Weather Report")
    print("Type a city name to get its current weather.")
    print("Type 'exit' to stop.")

    while True:
        city = input("\nEnter city name: ").strip()

        if city.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        try:
            show_weather(city)
        except HTTPError as error:
            print(f"Weather service returned an HTTP error: {error.code}")
        except URLError:
            print("Could not connect. Check your internet connection and try again.")
        except TimeoutError:
            print("The request timed out. Please try again.")
        except (json.JSONDecodeError, KeyError, ValueError) as error:
            print(f"Could not read the weather response: {error}")


if __name__ == "__main__":
    main()
