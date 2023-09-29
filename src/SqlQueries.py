

def create_tables(db_connector):
    table_names = ["User", "Activity", "TrackPoint"]
    table_definitions = [
        "user_id VARCHAR(255), has_labels boolean",
        "activity_id INT AUTO_INCREMENT, FOREIGN KEY (user_id) references USER(user_id), transportation_mode VARCHAR(255), start_date_time DATETIME, end_date_time DATETIME",
        "trackpoint_id INT AUTO_INCREMENT, FOREIGN KEY (activity_id) references Activity(activity_id), lat DOUBLE, lon DOUBLE, altitude INT, date_days DOUBLE, date_time DATETIME"
    ]
    try:
        for table_name, table_definition in table_names, table_definitions:
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition})"
            db_connector.cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table '{table_name}': {e}")


def insert_data(db_connector, table_name, data):
    try:
        db_connector.start_
        insert_query = f"INSERT INTO {table_name} VALUES ({data})"
        db_connector.cursor.execute(insert_query)
        db_connector.db_connection.commit()
        print(f"Data inserted into table '{table_name}' successfully.")
    except Exception as e:
        print(f"Error inserting data into table '{table_name}': {e}")
        db_connector.db_connection.rollback()
