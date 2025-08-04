import argparse
import json
import yaml
import os
from astrology_app_code import chart_engine


def load_input_data(file_path=None, args=None):
    if file_path:
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                return json.load(f)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(f)
    else:
        return {
            'date': args.date,
            'time': args.time,
            'city': args.city,
            'state': args.state,
            'lat': args.lat,
            'lon': args.lon
        }


def save_output(data, output_path):
    if output_path.endswith('.json'):
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    elif output_path.endswith('.yaml') or output_path.endswith('.yml'):
        with open(output_path, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)


def main():
    parser = argparse.ArgumentParser(description='Generate a natal astrology chart from birth info.')
    parser.add_argument('-f', '--file', help='Path to input JSON or YAML file with birth info')
    parser.add_argument('-d', '--date', help='Birth date (YYYY-MM-DD)')
    parser.add_argument('-t', '--time', help='Birth time (HH:MM)')
    parser.add_argument('-c', '--city', help='City of birth')
    parser.add_argument('-s', '--state', help='State of birth')
    parser.add_argument('--lat', type=float, help='Latitude')
    parser.add_argument('--lon', type=float, help='Longitude')
    parser.add_argument('--output1', default='natal_chart_summary.json', help='Output file for natal chart summary')
    parser.add_argument('--output2', default='fixed_star_conjunctions.json', help='Output file for fixed star conjunctions')

    args = parser.parse_args()
    input_data = load_input_data(args.file, args)

    # Generate astrology data
    chart_data = chart_engine.generate_chart(input_data)
    summary_data = chart_data.get("chart_metadata", {})
    conjunction_data = chart_data.get("fixed_star_conjunctions", [])

    # Save outputs
    save_output(summary_data, args.output1)
    save_output(conjunction_data, args.output2)


if __name__ == '__main__':
    main()
