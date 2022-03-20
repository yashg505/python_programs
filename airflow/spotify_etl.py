import sqlalchemy
import sqlite3
import pandas as pd
import datetime
import requests

def check_if_valid_data(df:pd.DataFrame) -> bool:
    if df.empty:
        print("No songs downloaded. Execution Finished")
        return False

    #Primary Key check:
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary key check is violated")
    
    #check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")
    
    #Check all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    timestamps = df['timestamps'].to_list()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("atleast one of the songs doesn't have yesterday's timeframe")
    
    return True

def run_spotify_etl():
    database_location = 'sqlite://my_played_tracks.sqlite'
    #with open(r'/Users/yashgourav/Documents/DE/airflow/dags/spotify_token.txt') as file:
    #    token = file.read()
    token = 'BQDLI6D9Ua8CJafa47j_9MfuRssRatxnPkfVHd0IM5EzX9qmbOmuazRJLspyq2yn6kZt4vRAA9AbnyNt4evB7cWPbLPSitZzvqUEQd6WjyuCpZV6FrtKo96BDQJj4TQHsaEfwO'
    headers = {
        "Accept":"application/json",
        "Content-Type":'application/json',
        "Authorization":"Bearer {token}.format(token=token)"
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp())*1000

    r = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?after={yesterday_unix_timestamp}", headers= headers)
    if r.status_code not in range(200, 299):
        raise Exception("API Token invalid")

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for songs in data.items():
        song_names.append(songs['track']['name'])
        artist_names.append(songs['track']['album']['artists'][0]['name'])
        played_at_list.append(songs['played_at'])
        timestamps.append(songs['played_at'][0:10])

    #prepare a dict
    song_dict = {
        "song_names":song_names,
        "artist_names":artist_names,
        "played_at_list":played_at_list,
        "timestamps":timestamps
    }

    songs_df = pd.DataFrame(song_dict, columns = ['songs_name','artist','plated_at','timestamp'])


    #validate the dataframe
    if check_if_valid_data(songs_df):
        print('dataframe is valid, proceed to storage')
    
    #load
    engine = sqlalchemy.create_engine(database_location)
    conn = sqlite3.connect()
    c = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    with conn:
        c.execute(sql_query)
    print('database created')

    try:
        songs_df.to_sql('my_played_tracks', engine=engine, index = False, if_exists='append')
    except:
        print("data Already in the database")
    
    conn.close()
    print('database closed successfully')
    
    