import pandas as pd
from helper_functions import get_15min, get_tickers, connect_postgres, connect_sqlalchemy

def get_15min_data():

    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_15min = pd.DataFrame()

    # Assigning values inside the dataframes
    list_15min = [get_15min(ticker) for ticker in currency_tickers]
    df_15min = df_15min.append(list_15min,ignore_index=True)
    df_15min['Timeframe']='15min'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_15min.to_sql('temp_15min', con=engine, index=False, if_exists='append',chunksize = 1000)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_15min(ticker,datetime,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_15min
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
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_15min;")
    upsert_cursor.execute("""DELETE from forex_15min 
                            where EXTRACT(MINUTES from forex_15min.datetime) NOT IN (0,15,30,45)
                            OR EXTRACT(SECOND from forex_15min.datetime) NOT IN(0);""")
    upsert_conn.close()