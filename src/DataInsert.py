# MAIN FILE FOR INSERTING THE DATA:

import pandas as pd
from DbConnector import DbConnector
import DataFetching as DaF
import SqlQueries as SQ
from pet_log import get_logger

ACTIVITY_LABELS = "start_date_time, end_date_time, user_id"
TRACKPOINT_LABELS = "activity_id, lat, lon, altitude, date_time"

logger = get_logger('main')

def insert_users():
    dbc = DbConnector()
    users = DaF.get_users()
    ## INSERT USERS TO DB
    SQ.create_tables(dbc)
    user_bulk = []
    for user in users:
        user_bulk.append((user, None))
    check, e = SQ.insert_bulk_data(dbc, 'User(user_id, has_labels)', user_bulk, "%s, %s")
    if check:
        logger.info("Successfully added users")
        return True
    else: 
        logger.error(f"Something went wrong when adding users. Exception: \n {e}")
        return False
    
def insert_activities_and_trackpoints(user):
    activities = DaF.get_activities(user)

def main():

    dbc = DbConnector()
    users = DaF.get_users()
    ## INSERT USERS TO DB
    SQ.create_tables(dbc)
    
    for user in users:
        check, e = SQ.insert_data(dbc, "User (user_id, has_labels)", (user, None), "%s, %s")    
        if not check:
            logger.error(f'Error in adding user:\n {e}')
            print(f'Stopping insert due to Exception:\n{e}')
            break
        activities = DaF.get_activities(user)
        
        for activity in activities:
            check, plotpoints = activity.get_track_points()
            if check: 
                activity_tuple = (activity.start, activity.end, activity.user)
                check, e = SQ.insert_data(dbc, "Activity ("+ACTIVITY_LABELS+")", activity_tuple, "%s, %s, %s")
                if check: 
                    ## INSERT ACTIVITY TO DB
                    ## BULK INSERT TRACKPOINTS TO DB
                    df = plotpoints
                    activity_id = SQ.get_last_rowid(dbc)
                    df.insert(0, 'activity_id', activity_id)
                    df['activity_id'] = activity_id
                    data_tuples = list(df.itertuples(index=False, name=None))
                    check, e = SQ.insert_bulk_data(dbc, "TrackPoint ("+TRACKPOINT_LABELS+")", data_tuples, "%s, %s, %s, %s, %s")
                    if not check: 
                        logger.error(f'Couldnt add trackpoints du to Exception\n {e}')
                else: 
                    logger.error(f'Couldnt add activity du to Exception:\n{e}')
            else:
                logger.info(f'Skipping activity: {activity.trackpoints} due to amount of points: {len(plotpoints)}')
    dbc.close_connection()

def update_labels():
    dbc = DbConnector()

    labeled_ids = DaF.get_labeled_ids()
    for user in labeled_ids:
        labels = DaF.get_labels(user)
        activities = SQ.get_activities(dbc, user)
        df = pd.DataFrame(activities, columns=["activity_id",  "user_id", "transportation_mode", "start_date_time", "end_date_time"])
        # Merge dataframes on start_date_time and end_date_time.
        merged_df = df.merge(labels, how = 'inner', on=["start_date_time", "end_date_time"])
        for index, row in merged_df.iterrows():
            SQ.update_transportation_mode(dbc, row["activity_id"], row["transportation_mode_y"])
            logger.info(f'Updated activity {row["activity_id"]} with transportation mode {row["transportation_mode_y"]}')
    dbc.close_connection()
        


update_labels()

# if __name__ == '__main__':
#     main()