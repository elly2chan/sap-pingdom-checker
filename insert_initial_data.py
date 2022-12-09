import json


def insert_initial_json_data_into_database(connection, cursor, json_file):
    with open(json_file) as json_f:
        json_data = json.load(json_f)
        for check in json_data['healthchecks']:
            cursor.execute('''INSERT OR IGNORE INTO healthchecks VALUES (?, ?, ?)''',
                           (check['name'], check['host'], check['type']))
            connection.commit()
