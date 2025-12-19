import argparse
import requests
import csv
from datetime import datetime
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', required=True)
    parser.add_argument('--country', required=True)
    parser.add_argument('--api-key', required=True)
    parser.add_argument('--output', default='weather_data.csv')  # Add this line
    
    args = parser.parse_args()
    
    print(f"Getting weather for {args.city}, {args.country}")
    
    # Your existing API call code here...
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save to specified output path
    with open(args.output, 'a', newline='') as csvfile:
        # Your existing CSV writing code here...
        pass
    
    print(f"Data saved to {args.output}")

if __name__ == "__main__":
    main()