import DbConnector as dbc
import SqlQueries as SQ

def main():
    db = dbc.DbConnector()
    SQ.create_tables(db)
    db.close_connection()

if __name__ == '__main__':
    main()