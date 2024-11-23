from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from station import *


class Application:
    def __init__(self):
        self.app = Flask(__name__)
        self.data_manager = DataManager()
        self.setup_routes()
        self.start_scheduler()

    def fetch_and_store_data(self):
        print("Fetching and storing data...")
        for sta_code in station_names.keys():
            station = Station()
            station.fetch_from_api(sta_code)
            self.data_manager.store_station(station)

    def start_scheduler(self):
        scheduler = BackgroundScheduler()
        interval = 30
        scheduler.add_job(self.fetch_and_store_data, 'interval', seconds=interval)
        print(f"Starting scheduler with interval of {interval} seconds.")
        scheduler.start()
    def setup_routes(self):
        @self.app.route('/')
        def index():
            self.fetch_and_store_data()
            station_dict = {}
            station_codes = station_names.keys()
            for code in station_codes:
                recent_entries = self.data_manager.fetch_recent_entries(code, 10)
                up_times = [entry.up_time for entry in recent_entries if entry.up_time] # this arr can be empty!!!!
                down_times = [entry.down_time for entry in recent_entries if entry.down_time] # this arr can be empty!!!
                is_delays = [entry.is_delay for entry in recent_entries if entry.is_delay]
                station_dict[code] = {
                    "up_times": up_times,
                    "down_times": down_times,
                    "is_delay": is_delays,
                }

            return render_template(
                'index.html',
                stations_info=station_dict,
                zip=zip
            )

    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == '__main__':
    application = Application()
    application.run()
