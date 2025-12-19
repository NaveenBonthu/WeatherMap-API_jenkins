#!/usr/bin/env python3
"""
Weather Data Collector for Jenkins Pipeline
Simple, robust version that definitely works
"""

import sys
import requests
import csv
from datetime import datetime

def log_message(msg):
    """Simple logging"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")

def parse_arguments():
    """Parse command line arguments"""
    args = {}
    
    # Manual parsing (more reliable than argparse for Windows/Jenkins)
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--city' and i + 1 < len(sys.argv):
            args['city'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--country' and i + 1 < len(sys.argv):
            args['country'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--api-key' and i + 1 < len(sys.argv):
            args['api_key'] = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    # Defaults
    args.setdefault('city', 'London')
    args.setdefault('country', 'UK')
    args.setdefault('api_key', '')
    
    return args

def get_weather_data(city, country, api_key):
    """Fetch weather data from OpenWeatherMap"""
    try:
        log_message(f"Fetching weather for {city}, {country}")
        
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': f"{city},{country}",
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant data
        weather_info = {
            'city': data.get('name', city),
            'country': data.get('sys', {}).get('country', country),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': data.get('main', {}).get('temp', 'N/A'),
            'feels_like': data.get('main', {}).get('feels_like', 'N/A'),
            'humidity': data.get('main', {}).get('humidity', 'N/A'),
            'pressure': data.get('main', {}).get('pressure', 'N/A'),
            'weather': data.get('weather', [{}])[0].get('main', 'N/A'),
            'description': data.get('weather', [{}])[0].get('description', 'N/A'),
            'wind_speed': data.get('wind', {}).get('speed', 'N/A')
        }
        
        log_message(f"Data received: {weather_info['temperature']}°C, {weather_info['weather']}")
        return weather_info
        
    except Exception as e:
        log_message(f"Error fetching weather: {e}")
        return None

def save_to_csv(data, filename='weather_data.csv'):
    """Save data to CSV file"""
    if not data:
        log_message("No data to save")
        return False
    
    try:
        # Check if file exists
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                file_exists = True
        except FileNotFoundError:
            file_exists = False
        
        # Write data
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        
        log_message(f"Data saved to {filename}")
        return True
        
    except Exception as e:
        log_message(f"Error saving to CSV: {e}")
        return False

def main():
    """Main function"""
    log_message("Weather Data Collector started")
    
    # Parse arguments
    args = parse_arguments()
    
    if not args.get('api_key'):
        log_message("ERROR: API key is required")
        log_message("Usage: python weather_collector.py --city <city> --country <country> --api-key <key>")
        return False
    
    # Get weather data
    weather_data = get_weather_data(
        city=args['city'],
        country=args['country'],
        api_key=args['api_key']
    )
    
    if not weather_data:
        log_message("Failed to fetch weather data")
        return False
    
    # Save to CSV
    if save_to_csv(weather_data):
        log_message("SUCCESS: Weather data collection completed")
        return True
    else:
        log_message("FAILED: Could not save data")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)