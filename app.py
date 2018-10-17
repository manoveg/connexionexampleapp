import connexion
import datetime
import logging
import requests

from connexion import NoContent


def get_pmvalues():
    ipv6_address = get_ipv6_address()
    lat_long = get_lat_long(ipv6_address)

    pm10_top5 = get_top5_pm10_values(lat_long)

    pm10_response = {}
    pm10_response_list = []

    for pm10vals in pm10_top5:


    return { "pm10": [{ "date": {"utc": "2018-10-16T23:00:00.000Z"},"value": 10.87,"unit": "µg/m³"}]}

def get_ipv6_address():
    ipv6address_json = None

    try:
        ipv6address_response = requests.get("https://ident.me/.json")

        if ipv6address_response.status_code == requests.codes.ok :
            ipv6address_json = ipv6address_response.json()
    except :
        logging.info("Request to get Ipv6 address unsuccessful.")
        raise

    return ipv6address_json["address"]

def get_lat_long(ipv6address):
    lat_long_json = {}
    url = "https://www.iplocate.io/api/lookup/" + ipv6address

    try:
        lat_long_response = requests.get(url)

        if lat_long_response.status_code == requests.codes.ok :
            lat_long_json = lat_long_response.json()

    except:
        logging.info("Request to get lattitude & longitude unsuccessful.")
        raise

    return lat_long_json

def get_top5_pm10_values(lat_long):

    lattitude = round(lat_long["latitude"],2)
    longitude = round(lat_long["longitude"],2)

    pm10val_json = {}
    pm10val_list = []

    #url = "https://api.openaq.org/v1/measurements?coordinates=" + str(lattitude) + "," + str(longitude)
    url = "https://api.openaq.org/v1/measurements?coordinates=52.53,13.41"

    try:
        pm10val_response = requests.get(url)

        if pm10val_response.status_code == requests.codes.ok :
            pm10val_json = pm10val_response.json()

    except:
        logging.info("Request to get pm10 values unsuccessful.")
        raise

    pm10val_list = pm10val_json["results"]

    sorted_list = sorted(pm10val_list, key = lambda x:x["value"],reverse=True)
    return sorted_list[:5]



logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')