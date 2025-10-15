import argparse
from configparser import *
from struct import *
import json
from urllib import parse, request
from urllib.request import urlopen
import sys

weather_URL = "http://api.openweathermap.org/data/2.5/weather"

def api_key():
    akey = ConfigParser()
    akey.read("secrets.ini")
    akey = akey["openweather"]["api"]
    return akey

def parse_args():
    parse = argparse.ArgumentParser(description="Gets city and weather info")
    parse.add_argument("Units", nargs="+", type=str, help= "Specify whether you'd like Imperial or Metric units")
    parse.add_argument("City",nargs="+", type=str,help="Enter name of city")
    return parse.parse_args()

def get_url(akey, city):
    """Use all parsed and gathered data to form URL"""

    units = sys.argv[1]
    url = f"{weather_URL}?q={city}&units={units}&appid={akey}"
    return url

def get_info(url):
    """Using the URL get the info on weather and split it into neat format"""
    page = urlopen(url)
    info = page.read()
    count = 0

    return json.loads(info)

def get_city():
    
    city = sys.argv[2]
    city = str(city)
    city_link = ""
    if len(sys.argv) > 3:
        addd = sys.argv[3]
        # city += str(sys.argv[2])
        city_link = f"{city}%20{addd}"
        city += f" {addd}"
    return city, city_link

if __name__== "__main__":
    key =api_key()
    args = parse_args()
    city, city_link = get_city()
    units = args.Units

    # differentiate between city's with more than one word in name
    if city_link:
        url = get_url(key, city_link)
    else:
        url = get_url(key,city)
    
    info = get_info(url)
    temperature = info["main"]["temp"]
    if units[0].lower() == "metric":
        temperature = f"{temperature}°С"
    else:
        temperature = f"{temperature}°F"
    rain = info["weather"][0]["description"]
    rain = rain.capitalize()
    print(f"City: {city}\nTemperature: {temperature}\n{rain}")
    