import sqlite3

from add_new_check import add_new_check_to_db
from insert_initial_data import insert_initial_json_data_into_database
from pingdom_checker import create_tables, \
    compare_pingdom_and_database_results_update_results_and_remove_unused_records, \
    compare_and_make_new_checks_in_pingdom_or_add_pingdom_checks_to_database


def main():

    # SET DATABASE CONFIGURATION
    connection = sqlite3.connect('pingdom_checker_db')
    cursor = connection.cursor()
    connection.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    row_cursor = connection.cursor()

    # SET API CONFIGURATION, PROVIDE YOUR OWN AUTHENTICATION TOKEN
    url = 'https://api.pingdom.com/api/3.1/checks'
    auth_token = 'put_your_auth_token_here'

    if connection is not None:
        create_tables(connection, cursor)
    else:
        print("Cannot connect to the database.")

    # INSERT INITIAL JSON DATA FROM 'healthchecks.json'
    insert_initial_json_data_into_database(connection, cursor, json_file='data/healthchecks.json')

    # COMPARE PINGDOM RESPONSE WITH DATABASE DATA AND UPDATE (ADD OR DELETE) RECORDS ACCORDING TO DIFFERENCES
    compare_pingdom_and_database_results_update_results_and_remove_unused_records(connection, cursor,
                                                                                  url, auth_token, row_cursor)

    # COMPARE PINGDOM RESPONSE WITH EXISTING DATABASE CHECKS AND UPDATE THEM ACCORDINGLY
    compare_and_make_new_checks_in_pingdom_or_add_pingdom_checks_to_database(row_cursor, url,
                                                                             auth_token, connection, cursor)

    '''
    IF YOU WANT TO ADD NEW CHECK, PROVIDE THE NEEDED PARAMETERS - NAME, HOST AND TYPE, BEFORE YOU START THE PROGRAM.
    WHEN ASKED, YOU SHOULD TYPE 'y' SO THAT THE CHECK IS SUCCESSFULLY ADDED TO THE DATABASE.
    '''

    new_check = input("Do you want to add a new check? (y/n): ")

    if new_check == 'y':
        check_name = None
        check_host = None
        check_type = None

        if type(check_name) == str and type(check_host) == str and type(check_type) == str:
            add_new_check_to_db(connection, cursor, check_name, check_host, check_type, row_cursor, url, auth_token)
        elif check_name is None and check_host is None and check_type is None:
            print("If you want to add new check you should provide check name, check host and check type.")
        else:
            raise TypeError("Please provide valid check name, check host and check type "
                            "to successfully add a new check to DB. Values must be strings.")

    connection.close()


if __name__ == '__main__':
    main()
