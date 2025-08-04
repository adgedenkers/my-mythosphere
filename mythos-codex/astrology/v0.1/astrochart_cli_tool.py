import argparse
import json
import yaml
import os
import astrochart_cli_engine as chart_engine


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


def save_output(data, filename_prefix):
    for key, value in data.items():
        if key == "fixed_star_conjunctions":
            file_name = f"{filename_prefix}__fixed_star_conjunctions.json"
        else:
            file_name = f"{filename_prefix}__{key}.json"
        with open(file_name, 'w') as f:
            json.dump(value, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Generate a natal astrology chart from birth info.')
    parser.add_argument('-f', '--file', help='Path to input JSON or YAML file with birth info')
    parser.add_argument('-d', '--date', help='Birth date (YYYY-MM-DD)')
    parser.add_argument('-t', '--time', help='Birth time (HH:MM)')
    parser.add_argument('-c', '--city', help='City of birth')
    parser.add_argument('-s', '--state', help='State of birth')
    parser.add_argument('--lat', type=float, help='Latitude')
    parser.add_argument('--lon', type=float, help='Longitude')
    parser.add_argument('--ephe', default='/home/adge/dev/astrology/swisseph', help='Path to Swiss Ephemeris data files')
    parser.add_argument('--prefix', default='natal_chart', help='Prefix for output files')

    args = parser.parse_args()
    input_data = load_input_data(args.file, args)

    # Generate astrology data
    chart_data = chart_engine.generate_chart(input_data, sweph_path=args.ephe)

    # Save all outputs
    save_output(chart_data, args.prefix)


if __name__ == '__main__':
    main()
