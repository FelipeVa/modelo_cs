import json


def main():
    create_zone_fie()


def create_zone_fie():
    obj = []
    cities = int(input('Number of cities: '))
    zone = input('Zone: ')

    for x in range(cities):
        city = input('Name of city #' + str(x + 1) + ': ')
        distance = float(input('Distance of ' + city + ': '))
        kits = int(input('Number of kits of ' + city + ': '))
        tolls = int(input('Value of tolls of ' + city + ': '))
        obj.append({
            'city': city.replace(' ', '_'),
            'distance': distance,
            'zone': zone.replace(' ', '_'),
            'kits': kits or 0,
            'tolls': {
                'total': tolls,
            }
        })

    generate_file(zone, obj)


def generate_file(file_name, obj):
    file = open('objects/zone_' + file_name.replace(' ', '_') + '.json', 'w')
    file.write(json.dumps(obj, indent=2, sort_keys=True))
    file.close()


if __name__ == '__main__':
    main()