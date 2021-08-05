import pandas as pd
from helper_functions import get_1week, get_tickers, connect_postgres, connect_sqlalchemy

def get_1week_data():

    # list of currency pairs
    currency_tickers = get_tickers()

    # Declaring the dataframes
    df_1week = pd.DataFrame()

    # Assigning values inside the dataframes
    list_1week = [get_1week(ticker) for ticker in currency_tickers]
    df_1week = df_1week.append(list_1week,ignore_index=True)
    df_1week['Timeframe']='1week'

    # Move dataframes to Postgres
    engine = connect_sqlalchemy()
    df_1week.to_sql('temp_weekly', con=engine, index=False, if_exists='append',chunksize = 1000)

    upsert_conn = connect_postgres()
    upsert_cursor = upsert_conn.cursor()
    insert_query = """Insert into forex_weekly(ticker,date,open,high,low,close,adj_close,volume,timeframe)
    select * from temp_weekly
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
    upsert_cursor.execute("DROP TABLE IF EXISTS temp_weekly;")
    upsert_conn.close()
