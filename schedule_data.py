import schedule
import time
from data_5min import get_5min_data
from data_15min import get_15min_data
from data_30min import get_30min_data
from data_60min import get_60min_data
from data_240min import get_240min_data
from data_1day import get_1day_data
from data_1week import get_1week_data
from data_1month import check_date


schedule.every(5).minutes.do(get_5min_data)
schedule.every(15).minutes.do(get_15min_data)
schedule.every(30).minutes.do(get_30min_data)
schedule.every(60).minutes.do(get_60min_data)
schedule.every(240).minutes.do(get_240min_data)
schedule.every().day.at("09:00").do(get_1day_data)
schedule.every().monday.at("09:00").do(get_1week_data)
schedule.every().sunday.at("09:00").do(check_date)

while 1:
    schedule.run_pending()
    time.sleep(1)
