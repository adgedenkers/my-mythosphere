import swisseph as swe
import datetime
import json
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import pandas as pd
import re

HOUSE_SYSTEM = "Placidus"
ZODIAC_TYPE = "Tropical"
EPHEMERIS = "Swiss Ephemeris"
INCLUDED_OBJECTS = [
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
    "Uranus", "Neptune", "Pluto", "Chiron", "Ceres", "Pallas", "Juno",
    "Vesta", "Lilith", "Mean Node", "Ascendant", "Midheaven", "Descendant", "IC"
]

def get_timezone_and_coords(city, region, country, date_str):
    geolocator = Nominatim(user_agent="astro_chart_generator")
    tf = TimezoneFinder()
    location = geolocator.geocode(f"{city}, {region}, {country}")
    if not location:
        raise ValueError("Location not found")
    lat, lon = location.latitude, location.longitude
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    timezone = pytz.timezone(timezone_str)
    local_dt = timezone.localize(datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M"))
    offset_hours = local_dt.utcoffset().total_seconds() / 3600
    return lat, lon, offset_hours, timezone_str

def get_sign(lon):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(lon // 30)]

def deg_min(lon):
    return f"{int(lon % 30)}°{int((lon % 1) * 60):02d}'"

def generate_chart(input_data, sweph_path="/usr/share/ephe"):
    swe.set_ephe_path(sweph_path)
    name = input_data["Name"]
    dob = input_data["Date of Birth"]
    tob = input_data["Time of Birth"]
    place = input_data["Place of Birth"]
    date_str = f"{dob} {tob}"
    lat, lon, tz_offset, tz_name = get_timezone_and_coords(place["City"], place["Region"], place["Country"], date_str)
    dt_utc = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M") - datetime.timedelta(hours=tz_offset)
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute / 60, swe.GREG_CAL)

    object_codes = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS, "Mars": swe.MARS,
        "Jupiter": swe.JUPITER, "Saturn": swe.SATURN, "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
        "Chiron": swe.CHIRON, "Ceres": 10001, "Pallas": 10002, "Juno": 10003, "Vesta": 10004,
        "Lilith": swe.MEAN_APOG, "Mean Node": swe.MEAN_NODE
    }

    positions = {}
    for obj, code in object_codes.items():
        pos, _ = swe.calc_ut(jd, code)
        positions[obj] = {"longitude": round(pos[0], 2), "retrograde": pos[3] < 0}

    HOUSE_SYSTEMS = {
        "Placidus": b'P',
        "Koch": b'K',
        "Whole": b'W',
        "Porphyry": b'O',
        "Equal": b'E'
    }

    system = HOUSE_SYSTEMS.get(HOUSE_SYSTEM, b'P')
    cusps, ascmc = swe.houses_ex(jd, lat, lon, system)

    positions["Ascendant"] = {"longitude": round(ascmc[0], 2), "retrograde": False}
    positions["Midheaven"] = {"longitude": round(ascmc[1], 2), "retrograde": False}
    positions["Descendant"] = {"longitude": round((ascmc[0] + 180) % 360, 2), "retrograde": False}
    positions["IC"] = {"longitude": round((ascmc[1] + 180) % 360, 2), "retrograde": False}

    house_spans = [(i + 1, cusps[i], cusps[(i + 1) % 12]) for i in range(12)]
    chart_objects = []
    for obj, pos in positions.items():
        lon = pos["longitude"]
        house = next((num for num, start, end in house_spans if start <= lon < (end if end > start else end + 360)), None)
        chart_objects.append({
            "Object": obj,
            "Sign": get_sign(lon),
            "Degrees": deg_min(lon),
            "Longitude": lon,
            "Retrograde": pos["retrograde"],
            "House": house
        })

    def parse_orb_to_decimal_safe(orb_str):
        if not isinstance(orb_str, str):
            return 1.0
        match = re.match(r"(\d+)°(\d+)?′?", orb_str)
        if not match:
            return 1.0
        degrees = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
        return degrees + minutes / 60.0

    stars_df = pd.read_csv("/mnt/data/astrology_app_code/astrology__fixed_stars.csv")
    stars_df["Decimal Orb"] = stars_df["Orb"].apply(parse_orb_to_decimal_safe)
    stars_df = stars_df[["Name", "Decimal Long", "Decimal Orb"]].dropna()

    conjunctions = []
    for obj in chart_objects:
        obj_lon = obj["Longitude"]
        for _, row in stars_df.iterrows():
            star_lon = float(row["Decimal Long"])
            orb = float(row["Decimal Orb"])
            diff = abs(obj_lon - star_lon)
            diff = min(diff, 360 - diff)
            if diff <= orb:
                conjunctions.append({
                    "Object": obj["Object"],
                    "Longitude": obj_lon,
                    "Star": row["Name"],
                    "Star_Longitude": star_lon,
                    "Orb": round(diff, 4)
                })

    conjunctions.sort(key=lambda x: x["Orb"])

    return {
        "chart_metadata": {
            "Name": name,
            "Birth": {
                "Date": dob,
                "Time": tob,
                "Place": place,
                "Latitude": lat,
                "Longitude": lon,
                "Timezone": tz_name
            },
            "House System": HOUSE_SYSTEM,
            "Zodiac Type": ZODIAC_TYPE,
            "Ephemeris": EPHEMERIS,
            "Included Objects": list(positions.keys()),
            "Excluded Objects": ["Part of Fortune", "Vertex", "Arabic Lots"],
            "Objects": chart_objects
        },
        "fixed_star_conjunctions": conjunctions
    }