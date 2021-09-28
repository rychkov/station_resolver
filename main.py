import json
import csv
import os

import requests as requests

URL = 'https://geocode-maps.yandex.ru/1.x'
API_KEY = os.environ['API_KEY']
API_KEY_PARAM_NAME = 'apikey'
FORMAT = 'json'
FORMAT_PARAM_NAME = 'format'
GEOCODE_PARAM_NAME = 'geocode'
result_json = open('result.json', 'w')


def process(row):
    station = 'жд станция ' + row[0] + ' ' + row[4]
    r = requests.get(URL, params={
        API_KEY_PARAM_NAME: API_KEY,
        FORMAT_PARAM_NAME: FORMAT,
        GEOCODE_PARAM_NAME: station
    })
    json.dump({row[0]: r.json()}, result_json)
    print(r.json(), sep='\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    station_csv = open('station.csv', 'r')
    csv_reader = csv.reader(station_csv)
    for row in csv_reader:
        process(row)

station_csv.close()

result_json.flush()
result_json.close()
