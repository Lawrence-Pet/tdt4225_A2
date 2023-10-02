# MAIN FILE FOR INSERTING THE DATA:

from DbConnector import DbConnector
import DataFetching as DaF
import SqlQueries as SQ

ACTIVITY_LABELS = "start_date_time, end_date_time, user_id"
TRACKPOINT_LABELS = "activity_id, lat, lon, altitude, date_time"

def main():

    dbc = DbConnector()
    users = DaF.get_users()
    ## INSERT USERS TO DB
    SQ.create_tables(dbc)
    
    for user in users:
        SQ.insert_data(dbc, "User (user_id, has_labels)", (user, None))    
        activities = DaF.get_activities(user)
        
        for activity in activities: 
            check, plotpoints = activity.get_track_points()
            if check: 
                activity_tuple = (activity.start, activity.end, activity.user)
                SQ.insert_data(dbc, "Activity ("+ACTIVITY_LABELS+")", activity_tuple)
                ## INSERT ACTIVITY TO DB
                ## BULK INSERT TRACKPOINTS TO DB
                df = plotpoints
                data_tuples = list(df.itertuples(index=False, name=None))
                SQ.insert_bulk_data(dbc, "TrackPoint ("+TRACKPOINT_LABELS+")", data_tuples, "%s, %s, %s, %s, %s")


if __name__ == '__main__':
    main()