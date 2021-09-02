import json


def main():
    create_zone_fie()


def create_zone_fie():
    obj = []
    cities = int(input('Number of cities: '))
    is_for_kits = int(input('Is for kits?: \n 1. Yes \n 2. No \n Type here: '))
    zone = 'default'

    if is_for_kits == 0:
        zone = input('Zone: ')

    for x in range(cities):
        city = input('Name of city #' + str(x + 1) + ': ')
        kits = int(input('Number of kits of ' + city + ': '))

        if is_for_kits == 1:
            obj.append({
                'city': city.replace(' ', '_'),
                'kits': kits or 0,
            })

        if is_for_kits == 0:
            distance = float(input('Distance of ' + city + ': '))
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

    generate_file(zone, obj, is_for_kits)


def generate_file(file_name, obj, is_for_kits):
    file_name_str = 'zone_' + file_name.replace(' ', '_') if is_for_kits == 0 else 'total_kits'
    file = open('objects/' + file_name_str + '.json', 'w')
    file.write(json.dumps(obj, indent=2, sort_keys=True))
    file.close()


if __name__ == '__main__':
    main()
