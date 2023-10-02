

def create_tables(db_connector):
    table_names = ["User", "Activity", "TrackPoint"]
    table_definitions = [
        "user_id VARCHAR(255) NOT NULL, has_labels boolean, PRIMARY KEY (user_id)",
        "activity_id INT NOT NULL AUTO_INCREMENT, user_id VARCHAR(255), transportation_mode VARCHAR(255), start_date_time DATETIME, end_date_time DATETIME, PRIMARY KEY (activity_id), FOREIGN KEY (user_id) references User(user_id)",
        "trackpoint_id INT NOT NULL AUTO_INCREMENT, activity_id INT, lat DOUBLE, lon DOUBLE, altitude INT, date_time DATETIME, PRIMARY KEY (trackpoint_id), FOREIGN KEY (activity_id) references Activity(activity_id)"
    ]
    try:
        for table_name, table_definition in zip(table_names, table_definitions):
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition})"
            db_connector.cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table '{table_name}': {e}")


def insert_data(db_connector, table_name, data):
    """
    Inserts one row to the database.
    """
    try:
        insert_query = f"INSERT INTO {table_name} VALUES {data}"
        db_connector.cursor.execute(insert_query)
        db_connector.db_connection.commit()
        print(f"Data inserted into table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error inserting data into table '{table_name}': {e}")
        db_connector.db_connection.rollback()

# 
def insert_bulk_data(db_connector, table_name, datatuples, format_string: str):
    """
    Inserts multiple rows to the database.
    """
    try:
        insert_query = f"INSERT INTO {table_name} VALUES ({format_string})"
        db_connector.cursor.executemany(insert_query, datatuples)
        db_connector.db_connection.commit()
        print(f"Data inserted into table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error inserting data into table '{table_name}': {e}")
        db_connector.db_connection.rollback()

