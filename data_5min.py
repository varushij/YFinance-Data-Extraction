import pandas as pd
from helper_functions import get_5min, get_tickers, connect_postgres, connect_sqlalchemy

def get_5min_data():
    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_5min = pd.DataFrame()

    # Assigning values inside the dataframes
    list_5min = [get_5min(ticker) for ticker in currency_tickers]
    df_5min = df_5min.append(list_5min,ignore_index=True)
    df_5min['Timeframe']='5min'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_5min.to_sql('temp_5min', con=engine, index=False, if_exists='append',chunksize = 1000)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_5min(ticker,datetime,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_5min
    on conflict (ticker, datetime)
    do update set
    ticker = EXCLUDED.ticker,
    datetime = EXCLUDED.datetime,
    open = EXCLUDED.open,
    high = EXCLUDED. high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    adj_close = EXCLUDED.adj_close,
    volume = EXCLUDED.volume,
    timeframe = EXCLUDED.timeframe;"""

    upsert_cursor.execute(insert_query)
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_5min;")
    upsert_cursor.execute("""DELETE from forex_5min 
                            where EXTRACT(MINUTES from forex_5min.datetime) NOT IN (0,5,10,15,20,25,30,35,40,45,50,55)
                            OR EXTRACT(SECOND from forex_5min.datetime) NOT IN(0);""")
    upsert_conn.close()