import requests
from datetime import datetime
from pymongo import MongoClient

station_names = {
    "KET": "Kennedy Town",
    "HKU": "HKU",
    "SYP": "Sai Ying Pun",
    "SHW": "Sheung Wan",
    "CEN": "Central",
    "ADM": "Admiralty",
    "WAC": "Wan Chai",
    "CAB": "Causeway Bay",
    # "ISL": "Island Line",
    "TIH": "Tin Hau",
    "FOH": "Fortress Hill",
    "NOP": "North Point",
    "QUB": "Quarry Bay",
    "TAK": "Tai Koo",
    "SWH": "Sai Wan Ho",
    "SKW": "Shau Kei Wan",
    "HFC": "Heng Fa Chuen",
    "CHW": "Chai Wan"
}


# record the station info at a certain time, an example of the fetched data is example_fetch.json
def _fetch_station_info(sta_code) -> list:
    url = "https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={}&sta={}&lang={}"
    line = "ISL"
    lang = "en"
    # print(url.format(line, s, lang))
    response = requests.get(url.format(line, sta_code, lang))
    data = response.json()
    return data


def cal_time_diff(cur_time: str, sys_time: str) -> str:
    current_time = datetime.strptime(sys_time, '%Y-%m-%d %H:%M:%S')
    parsed_time = datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S')
    time_difference = parsed_time - current_time
    # if the time is minus set is as 0
    if time_difference.days < 0:
        return "0:00:00"
    print("Time difference:", time_difference)
    return str(time_difference)


class Station:
    def __init__(self):
        # time is the 'sys_time' in the dataset
        self.sys_time = None
        self.station_line = None
        # e.g. "KET"
        self.station_code = None
        # up_time is the str of the time of the next train
        self.up_time = None
        self.down_time = None
        # is_delay is an arr where the index is the station code and the value is a boolean
        self.is_delay = []

    def __str__(self):
        return f"Station: {self.station_code}, Line: {self.station_line}, sys_time: {self.sys_time}, up_time: {self.up_time}, down_time: {self.down_time}, is_delay: {self.is_delay}"

    def fetch_from_api(self, p_station_code, p_station_line="ISL"):
        self.station_line = p_station_line
        self.station_code = p_station_code
        data = _fetch_station_info(p_station_code)
        if 'sys_time' in data:
            self.sys_time = data['sys_time']
        if 'isdelay' in data:
            self.is_delay = data['isdelay']

        if 'data' in data:
            station_data = data['data'][p_station_line + "-" + p_station_code]

            if 'UP' in station_data:
                self.up_time = station_data['UP'][0]['time']
            if 'DOWN' in station_data:
                self.down_time = station_data['DOWN'][0]['time']

        else:
            print(f"No data available for station code: {p_station_code}")

class DataManager:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["mtr"]
            self.collection = self.db["stations"]
        except Exception as e:
            print(f"Warning: Failed to connect to MongoDB: {e}")

    def store_station(self, station) -> None:
        station_data = {
            "station_code": station.station_code,
            "station_line": station.station_line,
            "sys_time": station.sys_time,
            "up_time": station.up_time,
            "down_time": station.down_time,
            "is_delay": station.is_delay
        }
        self.collection.insert_one(station_data)

    def fetch_station(self, station_code) -> Station:
        record = self.collection.find_one({"station_code": station_code})
        if record:
            station = Station()
            station.station_code = record.get("station_code")
            station.station_line = record.get("station_line")
            station.sys_time = record.get("sys_time")
            station.up_time = record.get("up_time")
            station.down_time = record.get("down_time")
            station.is_delay = record.get("is_delay", [])
            return station
        else:
            print(f"No record found for station code: {station_code}")
            return None

    def fetch_recent_entries(self, station_code, limit=10):
        records = self.collection.find({"station_code": station_code}).sort("sys_time", -1).limit(limit)
        stations = []
        for record in records:
            station = Station()
            station.station_code = record.get("station_code")
            station.station_line = record.get("station_line")
            station.sys_time = record.get("sys_time")
            station.up_time = record.get("up_time")
            station.down_time = record.get("down_time")
            station.is_delay = record.get("is_delay", [])
            stations.append(station)
        return stations

    # for debug
    # def is_connected(self):
    #     try:
    #         self.client.admin.command('ping')
    #         return True
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return False