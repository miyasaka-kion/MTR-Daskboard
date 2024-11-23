import app
from datetime import datetime



def test_get_station_info():
    info = app.get_station_info()
    for sta_code, cur_info in zip(app.station_names.keys(), info):
        if 'data' not in cur_info:
            print("No data for", sta_code)
            continue
        for sta_key, data in cur_info['data'].items():
            print(sta_key)
            if 'UP' in data:
                print("UP time", data['UP'][0]['time'])
                print(app.cal_time_diff(data['UP'][0]['time']))
            if 'DOWN' in data:
                print("DOWN time", data['DOWN'][0]['time'])
                print(app.cal_time_diff(data['DOWN'][0]['time']))




if __name__ == "__main__":
    test_get_station_info()