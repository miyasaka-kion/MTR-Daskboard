from flask import Flask, render_template, jsonify
import requests
from datetime import datetime


app = Flask(__name__)

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

# record the station info at a certain time
class StationInfo:
    pass

def cal_time_diff(cur_time: str, sys_time: str) -> str:
    current_time = datetime.strptime(sys_time, '%Y-%m-%d %H:%M:%S')
    parsed_time = datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S')
    time_difference = parsed_time - current_time
    # if the time is minus set is as 0
    if time_difference.days < 0:
        return "0:00:00"
    print("Time difference:", time_difference)
    return str(time_difference)

def get_station_info() -> list:
    url = "https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={}&sta={}&lang={}"
    line = "ISL"
    lang = "en"
    dataset = []
    for s in station_names.keys():
        # print(url.format(line, s, lang))
        response = requests.get(url.format(line, s, lang))
        data = response.json()
        # print(data)
        dataset.append(data)
    return dataset


@app.route('/')
def index():
    all_info = get_station_info()
    for station in all_info:
        if 'data' in station:
            for sta_key, data in station['data'].items():
                if 'sys_time' in data:
                    sys_time = data['sys_time']
                else:
                    print("Fail to get sys_time")
                    continue

                if 'UP' in data:
                    time = cal_time_diff(data['UP'][0]['time'], sys_time)
                    data['UP'][0]['time_diff'] = cal_time_diff(data['UP'][0]['time'], sys_time)
                if 'DOWN' in data:
                    data['DOWN'][0]['time_diff'] = cal_time_diff(data['DOWN'][0]['time'], sys_time)
    return render_template('index.html', stations=station_names, info=all_info, zip=zip)


if __name__ == '__main__':
    app.run(debug=True)


