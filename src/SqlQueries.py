

def create_tables(db_connector, table_definition):
    table_names = ["User", "Activity", "TrackPoint"]
    table_definitions = [
        "id VARCHAR(255), has_labels boolean",
        "id INT AUTO_INCREMENT, FOREIGN KEY (user_id) references USER(id), transportation_mode VARCHAR(255), start_date_time DATETIME, end_date_time DATETIME",
        "id INT AUTO_INCREMENT, FOREIGN KEY (activity_id) references Activity(id), lat DOUBLE, lon DOUBLE, altitude INT, date_days DOUBLE, date_time DATETIME"
    ]
    try:
        for table_name, table_definition in table_names, table_definitions:
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition})"
            db_connector.cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table '{table_name}': {e}")