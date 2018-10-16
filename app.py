import connexion
import datetime
import logging

from connexion import NoContent


def get_pmvalues():

    return { "pm10": [{ "date": {"utc": "2018-10-16T23:00:00.000Z"},"value": 10.87,"unit": "µg/m³"}]}



logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')