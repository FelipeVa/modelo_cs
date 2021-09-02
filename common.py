import json


def file_selector():
    d = dict()

    d['file'] = int(input('Which file do you want to model: '
                          '\n 1. Norte '
                          '\n 2. Centro Tulua'
                          '\n 3. Centro Buga '
                          '\n 4. Sur Oriente '
                          '\n 5. Sur Occidente '
                          '\n 6. Kits '
                          '\n\nType here: '))

    d['file_list'] = {
        1: 'zone_norte',
        2: 'zone_centro_tulua',
        3: 'zone_centro_buga',
        4: 'zone_sur_oriente',
        5: 'zone_sur_occidente',
        6: 'kits'
    }

    return d


def get_object_from_file(file_path):
    file = ''

    # File where the zone object is located
    file_path = 'objects/' + file_path + '.json'

    # Check if zone file exist
    try:
        file = open(file_path)
        # Do something with the file
    except IOError:
        print('This zone file doesnt exist yet, please create it first.')
        exit()

    json_object = json.loads(file.read())

    file.close()

    return json_object


def file_loader(zone, zone_list):
    file = ''
    # File where the zone object is located
    file_path = 'objects/' + zone_list[zone] + '.json'

    # Check if zone file exist
    try:
        file = open(file_path)
        # Do something with the file
    except IOError:
        print('This zone file doesnt exist yet, please create it first.')
        exit()

    zone_object = json.loads(file.read())

    file.close()

    return zone_object


def create_result_json_file(obj, file_name):
    create_json_file(obj, 'objects/results/' + file_name)


def create_json_file(obj, file_path):
    file = open(file_path + '.json', 'w')
    file.write(json.dumps(obj, indent=2, sort_keys=True))
    file.close()
