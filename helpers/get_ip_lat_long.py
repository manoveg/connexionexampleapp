import logging
import requests


# This function returns the ipv6 address
def get_ipv6_address():

    ipv6address_json = None

    try:
        ipv6address_response = requests.get("https://ident.me/.json")

        if ipv6address_response.status_code == requests.codes.ok :
            ipv6address_json = ipv6address_response.json()

    except requests.exceptions.Timeout:
        logging.info("Request to get Ipv6 address unsuccessful due to timeout.")
    except requests.exceptions.TooManyRedirects:
        logging.info("Request to getIpv6 address unsuccessful because of too many redirects.")
    except requests.exceptions.RequestException as e:
        logging.info("Request to get Ipv6 address unsuccessful")

    return ipv6address_json["address"]

# This function returns lattitude and longitude based on ipv6 address
def get_lat_long(ipv6address):

    lat_long_json = {}
    url = "https://www.iplocate.io/api/lookup/" + ipv6address

    try:
        lat_long_response = requests.get(url)

        if lat_long_response.status_code == requests.codes.ok :
            lat_long_json = lat_long_response.json()

    except requests.exceptions.Timeout:
        logging.info("Request to get lattitude & longitude unsuccessful due to timeout.")
    except requests.exceptions.TooManyRedirects:
        logging.info("Request to get lattitude & longitude unsuccessful because of too many redirects.")
    except requests.exceptions.RequestException as e:
        logging.info("Request to getlattitude & longitude unsuccessful")

    logging.info(lat_long_json)
    return lat_long_json

# This function gets top5 PM10 values fetched for the lattitude and longitude passed as argument
def get_top5_pm10_values(lat_long):

    # rounding off the lattitude and longitude to 2 decimal places as otherwise api was not returning any result
    lattitude = round(lat_long["latitude"],2)
    longitude = round(lat_long["longitude"],2)

    pm10val_json = {}

    url = "https://api.openaq.org/v1/measurements?coordinates=" + str(lattitude) + "," + str(longitude)

    # Hardcoded value to test for Berlin
    #url = "https://api.openaq.org/v1/measurements?coordinates=52.53,13.41"

    try:
        pm10val_response = requests.get(url)

        if pm10val_response.status_code == requests.codes.ok :
            pm10val_json = pm10val_response.json()

    except requests.exceptions.Timeout:
        logging.info("Request to get pm10 values unsuccessful due to timeout.")
    except requests.exceptions.TooManyRedirects:
        logging.info("Request to get pm10 values unsuccessful because of too many redirects.")
    except requests.exceptions.RequestException as e:
        logging.info("Request to get pm10 values unsuccessful")


    if not pm10val_json:
        return []


    pm10val_list = pm10val_json["results"]

    # sorting in descing order to get top 5 PM10 values
    sorted_list = sorted(pm10val_list, key = lambda x:x["value"],reverse=True)
    return sorted_list[:5]
