import pandas as pd
from helper_functions import get_1day, get_tickers, connect_postgres, connect_sqlalchemy
import schedule
import time

def get_1day_data():
    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_1day = pd.DataFrame()

    # Assigning values inside the dataframes
    list_1day = [get_1day(ticker) for ticker in currency_tickers]
    df_1day = df_1day.append(list_1day,ignore_index=True)
    df_1day['TimeFrame'] = '1day'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_1day.to_sql('temp_daily', con=engine, index=False, if_exists='append',chunksize = 1000)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_daily(ticker,date,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_daily
    on conflict (ticker, date)
    do update set
    ticker = EXCLUDED.ticker,
    date = EXCLUDED.date,
    open = EXCLUDED.open,
    high = EXCLUDED. high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    adj_close = EXCLUDED.adj_close,
    volume = EXCLUDED.volume,
    timeframe = EXCLUDED.timeframe;"""

    upsert_cursor.execute(insert_query)
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_daily;")
    upsert_conn.close()