from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api,clean_daily_db,getting_btc_data
from pytz import utc
from apscheduler.triggers.cron import CronTrigger

def start():
	scheduler = BackgroundScheduler()
	scheduler.configure(timezone=utc)
	# scheduler.add_job(schedule_api, 'interval', minutes=15)
	# scheduler.add_job(clean_daily_db, 'interval', minutes=1)
	
	# scheduler.add_job(getting_btc_data, 'interval', minutes=1)
	
	# scheduler.add_job(Telegram_data, 'interval', minutes=5)
	# scheduler.add_job(clean_daily_db,  CronTrigger.from_crontab('* 10 * * *'))
	scheduler.start()
