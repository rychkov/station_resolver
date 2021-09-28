import json

STATION_2_DATA_MAP = {}
DEFAULT_LOCATION_TUPLE = (55.7537, 37.6199)


def parse_candidate(candidate):
    kind = candidate['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind']
    if kind == 'railway_station':
        point = candidate['GeoObject']['Point']['pos'].split()
        print("candidate = " + str(candidate) + "\n")
        return float(point[1]), float(point[0])
    return 0, 0


def get_point(response):
    try:
        meta = response['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']
        print("Found candidates " + meta['found'] + " for " + meta['request'])
        for candidate in response['response']['GeoObjectCollection']['featureMember']:
            (lat, lon) = parse_candidate(candidate)
            if lat != 0 and lon != 0:
                return lat, lon
        return DEFAULT_LOCATION_TUPLE
    except KeyError:
        # skip
        return DEFAULT_LOCATION_TUPLE


def parse_json(value):
    for k in value.keys():
        if k != 'NAME':
            STATION_2_DATA_MAP[k] = get_point(value[k])


def load_json():
    json_file = open('p.json', 'r')
    s = ''
    while True:
        line = json_file.readline()
        if line is None or line == '':
            break
        parse_json(json.loads(line))
    json_file.close()


load_json()

for k in STATION_2_DATA_MAP:
    print("UPDATE station SET latitude = '", STATION_2_DATA_MAP[k][0],
          "', longitude = '", STATION_2_DATA_MAP[k][1], "' WHERE name = '", k.strip(), "';", sep='')
