import pandas as pd
from helper_functions import get_30min, get_tickers, connect_postgres, connect_sqlalchemy

def get_30min_data():
    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_30min = pd.DataFrame()

    # Assigning values inside the dataframes
    list_30min = [get_30min(ticker) for ticker in currency_tickers]
    df_30min = df_30min.append(list_30min,ignore_index=True)
    df_30min['Timeframe']='30min'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_30min.to_sql('temp_30min', con=engine, index=False, if_exists='append',chunksize = 1000)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_30min(ticker,datetime,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_30min
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
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_30min;")
    upsert_cursor.execute("""DELETE from forex_30min 
                            where EXTRACT(MINUTES from forex_30min.datetime) NOT IN (0,30)
                            OR EXTRACT(SECOND from forex_30min.datetime) NOT IN(0);""")
    upsert_conn.close()