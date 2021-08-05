import pandas as pd
from helper_functions import get_60min, get_tickers, connect_postgres, connect_sqlalchemy

def get_240min_data():
    
    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_240min = pd.DataFrame()

    # Assigning values inside the dataframes
    list_240min = [get_60min(ticker) for ticker in currency_tickers]
    df_240min = df_240min.append(list_240min,ignore_index=True)
    df_240min['Timeframe']='240min'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_240min.to_sql('temp_240', con=engine, if_exists='append',index=False)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_240min(ticker,datetime,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_240min
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
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_240min;")
    upsert_cursor.execute("""DELETE from forex_240min 
                            where EXTRACT(HOURS from forex_240min.datetime) NOT IN (0,4,8,12,16,20)
                            OR EXTRACT(MINUTES from forex_240min.datetime) NOT IN (0)
                            OR EXTRACT(SECOND from forex_240min.datetime) NOT IN (0);""")
    upsert_conn.close()