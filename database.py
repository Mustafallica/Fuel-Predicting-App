import sqlite3
from aifc import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def showTable(conn, showTable):
    try:
        users = []
        c = conn.cursor()
        c.execute(showTable)
        rows = c.fetchall()
        for row in rows:
            users.append(row)

        print(users)

    except Error as e:
        print(e)


def main():
    database = "client1.db"

    ShowTable = """ select * from User """

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS User (
                                        id integer PRIMARY KEY,
                                        email text NOT NULL,
                                        Password text NOT NULL

                                    ); """
    sql_create_projects_client = """ CREATE TABLE IF NOT EXISTS ClientInfo (
                                            id integer PRIMARY KEY,
                                            Firstname text NOT NULL,
                                            Lastname text NOT NULL,
                                            Email text NOT NULL,
                                            Address text NOT NULL,
                                            Address1 text NOT NULL,
                                            city text NOT NULL,
                                            state text NOT NULL,
                                            zipcode text NOT NULL
                                            

                                        ); """
    sql_FuelQoute = """ CREATE TABLE IF NOT EXISTS FuelQoute (
                                                id integer PRIMARY KEY,
                                                gallonreq integer NOT NULL,
                                                Address text NOT NULL,
                                                City text NOT NULL,
                                                date text NOT NULL,
                                                price real NOT NULL,
                                                totalprice real NOT NULL
                                                
                                                
                                            ); """

    sql_FuelQoute1 = """ CREATE TABLE IF NOT EXISTS FuelQoute1 (
                                                    id integer PRIMARY KEY,
                                                    gallonreq integer NOT NULL,
                                                    email text NOT NULL,
                                                    Address text NOT NULL,
                                                    City text NOT NULL,
                                                    date text NOT NULL,
                                                    price real NOT NULL,
                                                    totalprice real NOT NULL


                                                ); """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:

        showTable(conn, ShowTable)

        # create projects table
        #create_table(conn, sql_create_projects_table)
        # create tasks table
       # create_table(conn,sql_create_projects_client)
        #create_table(conn, sql_FuelQoute1)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
