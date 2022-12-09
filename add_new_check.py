from pingdom_checker import compare_and_make_new_checks_in_pingdom_or_add_pingdom_checks_to_database


def add_new_check_to_db(connection, cursor, name, host, check_type, row_cursor, url, auth_token):
    cursor.execute('''INSERT OR IGNORE INTO healthchecks VALUES (?, ?, ?)''',
                   (name, host, check_type))
    connection.commit()

    compare_and_make_new_checks_in_pingdom_or_add_pingdom_checks_to_database(row_cursor, url, auth_token,
                                                                             connection, cursor)
