# -*- coding: utf-8 -*-

"""Flask app to get highest 5 PM10 values for an ip address
This app uses Zalando's open source connexion project which is a
Swagger/OpenAPI First framework for Python on top of Flask with automatic endpoint validation
The swagger yaml file is in swagger directory. This helps in following ways:
->simplify the development process
->confirm expectations about what your API will look like
url: https://github.com/zalando/connexion
"""
import connexion
import logging
from helpers.get_ip_lat_long import get_ipv6_address
from helpers.get_ip_lat_long import get_top5_pm10_values
from helpers.get_ip_lat_long import get_lat_long
from connexion import NoContent


def get_pmvalues():

    pm10_response = {}
    pm10_response_list = []
    pm10_response["pm10"] = []

    ipv6_address = get_ipv6_address()
    lat_long = get_lat_long(ipv6_address)

    pm10_top5 = get_top5_pm10_values(lat_long)

    if not pm10_top5:
        return NoContent, 204

    for pm10vals in pm10_top5:
        pm10_response_list.append({"date":{"utc":pm10vals["date"]["utc"]},"unit":pm10vals["unit"],"value":pm10vals["value"]})

    pm10_response["pm10"] = pm10_response_list

    return pm10_response


logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('swagger.yaml', validate_responses=True)
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')