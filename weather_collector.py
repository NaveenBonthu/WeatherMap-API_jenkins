import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Weather Data Collector')
    parser.add_argument('--city', default='London', help='City name')
    parser.add_argument('--country', default='UK', help='Country code')
    parser.add_argument('--api-key', required=True, help='OpenWeatherMap API key')
    parser.add_argument('--output', default='weather_data.csv', help='Output CSV filename')
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    print(f"Starting weather collection for {args.city}, {args.country}")
    
    # Your existing code here, using args.city, args.country, args.api_key
    collector = WeatherDataCollector(
        api_key=args.api_key,
        city=args.city,
        country_code=args.country
    )
    
    weather_data = collector.get_weather_data()
    if weather_data:
        collector.save_to_csv(weather_data, args.output)

if __name__ == "__main__":
    main()