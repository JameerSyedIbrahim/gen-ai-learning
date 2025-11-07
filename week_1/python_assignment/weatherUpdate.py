#!/usr/bin/env python3
"""
Quick weather using wttr.in (no API key).
"""

import requests
import argparse
import sys

WTTR_URL = "https://wttr.in/{}?format=j1"  # returns JSON

def get_wttr(city: str):
    url = WTTR_URL.format(city)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def format_wttr(data: dict):
    # wttr.in structure: current_condition is a list with a single dict
    current = data.get("current_condition", [{}])[0]
    temp_C = current.get("temp_C")
    temp_F = current.get("temp_F")
    weather_desc = current.get("weatherDesc", [{}])[0].get("value", "")
    humidity = current.get("humidity")
    feels_like_C = current.get("FeelsLikeC")
    wind_kmph = current.get("windspeedKmph")
    precip_mm = current.get("precipMM")

    return (
        f"Condition: {weather_desc}\n"
        f"Temperature: {temp_C} °C / {temp_F} °F\n"
        f"Feels like: {feels_like_C} °C\n"
        f"Humidity: {humidity}%\n"
        f"Wind: {wind_kmph} km/h\n"
        f"Precipitation: {precip_mm} mm\n"
    )

def main():
    parser = argparse.ArgumentParser(description="Show weather via wttr.in (no API key).")
    parser.add_argument("city", help="City name (e.g., 'Chennai' or 'London')")
    args = parser.parse_args()

    try:
        data = get_wttr(args.city)
    except requests.HTTPError as e:
        print("HTTP error:", e)
        sys.exit(1)
    except requests.RequestException as e:
        print("Network error:", e)
        sys.exit(1)

    print(format_wttr(data))

if __name__ == "__main__":
    main()
