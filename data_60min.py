import pandas as pd
from helper_functions import get_60min, get_tickers, connect_postgres, connect_sqlalchemy

def get_60min_data():

    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_60min = pd.DataFrame()

    # Assigning values inside the dataframes
    list_60min = [get_60min(ticker) for ticker in currency_tickers]
    df_60min = df_60min.append(list_60min,ignore_index=True)
    df_60min['Timeframe']='60min'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_60min.to_sql('temp_60min', con=engine, index=False, if_exists='append',chunksize = 1000)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_60min(ticker,datetime,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_60min
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
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_60min;")
    upsert_cursor.execute("""DELETE from forex_60min 
                            where EXTRACT(MINUTES from forex_60min.datetime) NOT IN (0)
                            OR EXTRACT(SECOND from forex_60min.datetime) NOT IN (0);""")
    upsert_conn.close()