# MAIN FILE FOR INSERTING THE DATA:

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

        check, e = SQ.insert_data(dbc, "User (user_id, has_labels)", (user, None))    
        if not check:
            logger.error(f'Error in adding user:\n {e}')
            print(f'Stopping insert due to Exception:\n{e}')
            break

        activities = DaF.get_activities(user)
        
        for activity in activities: 
            check, plotpoints = activity.get_track_points()
            if check: 
                activity_tuple = (activity.start, activity.end, activity.user)
                check, e = SQ.insert_data(dbc, "Activity ("+ACTIVITY_LABELS+")", activity_tuple)
                if check: 
                    ## INSERT ACTIVITY TO DB
                    ## BULK INSERT TRACKPOINTS TO DB
                    df = plotpoints
                    data_tuples = list(df.itertuples(index=False, name=None))
                    check, e = SQ.insert_bulk_data(dbc, "TrackPoint ("+TRACKPOINT_LABELS+")", data_tuples, "%s, %s, %s, %s, %s")
                    if not check: 
                        logger.error(f'Couldnt add trackpoints du to Exception\n {e}')
                else: 
                    logger.error(f'Couldnt add activity du to Exception:\n{e}')
            else:
                logger.info(f'Skipping activity: {activity}')
    dbc.close_connection()

if __name__ == '__main__':
    main()