import requests


def create_tables(connection, cursor):
    healthcheck_table = '''CREATE TABLE IF NOT EXISTS healthchecks(name text, host text unique, type text)'''
    results_table = '''CREATE TABLE IF NOT EXISTS results(id text, name text, host text unique, type text, status text)'''
    cursor.execute(healthcheck_table)
    cursor.execute(results_table)
    connection.commit()


def get_current_results_hosts_from_database(row_cursor):
    current_results_in_database = row_cursor.execute('''SELECT * FROM results''').fetchall()
    results_hosts = []

    for check in current_results_in_database:
        results_hosts.append(check['host'])

    return results_hosts


def compare_pingdom_and_database_results_update_results_and_remove_unused_records(connection, cursor,
                                                                                  url, auth_token, row_cursor):
    all_created_checks = requests.get(url, auth=(auth_token, ''))
    response = all_created_checks.json()
    response = [{k: v for k, v in check.items() if k in {'id', 'name', 'hostname', 'type', 'status'}} for check in
                response['checks']]

    for check in response:
        cursor.execute('''INSERT OR IGNORE INTO results VALUES (?, ?, ?, ?, ?)''',
                       (check['id'], check['name'], check['hostname'], check['type'], check['status']))
        cursor.execute('''UPDATE results SET status = ? WHERE host = ?''', (check['status'], check['hostname'], ))
        connection.commit()

    database_hostnames = get_current_results_hosts_from_database(row_cursor)
    response_hostnames = [check['hostname'] for check in response]

    differences = list(set(database_hostnames).difference(response_hostnames))
    if differences:
        for host in differences:
            cursor.execute('''DELETE FROM healthchecks WHERE host = ?''', (host,))
            cursor.execute('''DELETE FROM results WHERE host = ?''', (host,))
            connection.commit()


def compare_and_make_new_checks_in_pingdom_or_add_pingdom_checks_to_database(row_cursor, url,
                                                                             auth_token, connection, cursor):
    healthchecks = row_cursor.execute('''SELECT * FROM healthchecks''').fetchall()

    results_hosts = get_current_results_hosts_from_database(row_cursor)

    for check in healthchecks:
        if check['host'] not in results_hosts:
            requests.post(url, data=check, auth=(auth_token, ''))

    healthchecks_hosts = [check['host'] for check in healthchecks]

    differences = list(set(results_hosts).difference(healthchecks_hosts))
    if differences:
        for host in differences:
            cursor.execute('''INSERT INTO healthchecks (name, host, type)
            SELECT name, host, type FROM results WHERE host = ?''', (host,))

    compare_pingdom_and_database_results_update_results_and_remove_unused_records(connection, cursor,
                                                                                  url, auth_token, row_cursor)
