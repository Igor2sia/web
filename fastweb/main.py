import requests
import json
import datetime

from flask import jsonify


def get_info(from_station, to_station):
    current_date = str(datetime.datetime.now().date())
    url = 'https://api.rasp.yandex.net/v3.0/stations_list/?apikey=dde7d57e-2d28-4d6a-a8f9-fb884b810c24&lang=ru_RU&format=json'
    res = requests.get(url)
    k = json.loads(res.text)
    code_station_to = None
    code_station_from = None
    for i in k['countries']:
        if i['title'] == 'Россия':
            for d in i['regions']:
                if code_station_from and code_station_to:
                    break
                if d['title'] == 'Москва и Московская область':
                    for c in d['settlements']:
                        if code_station_from and code_station_to:
                            break
                        for l in c['stations']:
                            if code_station_from and code_station_to:
                                break
                            if from_station.lower() in l['title'].lower() and 'МЦК' not in l['direction'] and l['transport_type'] == 'train':
                                code_station_from = l['codes']['yandex_code']
                            elif to_station.lower() in l['title'].lower() and 'МЦК' not in l['direction'] and l['transport_type'] == 'train':
                                code_station_to = l['codes']['yandex_code']
            break
    info_train = get_info_train(f"https://api.rasp.yandex.net/v3.0/search/?apikey=cb576e43-d018-4e34-b93c-0896c81ba918&format=json&limit=200&from={code_station_from}&to={code_station_to}&lang=ru_RU&date={current_date}")

    print(info_train)

    return info_train

def get_info_train(url_rasp):
    res_rasp = requests.get(url_rasp)
    res_rasp = json.loads(res_rasp.text)
    hour = int(datetime.datetime.now().hour)
    min = int(datetime.datetime.now().minute)

    if 'segments' not in res_rasp:
        return jsonify({'error': 'Invalid data format'}), 400

    for train in res_rasp['segments']:
        hour_train1 = int(train['departure'].split('T')[1].split(':')[0])
        min_train1 = int(train['departure'].split('T')[1].split(':')[1])
        hour_train2 = int(train['arrival'].split('T')[1].split(':')[0])
        min_train2 = int(train['arrival'].split('T')[1].split(':')[1])



        if int(hour_train1) == hour:
            if int(min_train1) > min:
                return jsonify({'value': f"Твоя электричка будет типа({train['thread']['transport_subtype']['title']})\nмаршрута {train['thread']['title']}\nприбудет на станцию {train['from']['title']} в {hour_train1}:{min_train1}, прибудет на станцию {train['to']['title']} в {hour_train2}:{min_train2} и будет стоить {train['tickets_info']['places'][0]['price']['whole']} рублей.\n Время в пути составит {calculate_travel_time(hour_train1, min_train1, hour_train2, min_train2)}"}), 200
                break
        elif int(hour_train1) > hour:
            return jsonify({'value': f"Твоя электричка будет {train['thread']['transport_subtype']['title']}\nмаршрута {train['thread']['title']}\nприбудет на станцию {train['from']['title']} в {hour_train1}:{min_train1}, прибудет на станцию {train['to']['title']} в {hour_train2}:{min_train2} и будет стоить {train['tickets_info']['places'][0]['price']['whole']} рублей.\n Время в пути составит {calculate_travel_time(hour_train1, min_train1, hour_train2, min_train2)}"}), 200
            break

def calculate_travel_time(start_hours, start_minutes , end_hours, end_minutes):

    start_total_minutes = (start_hours) * 60 + (start_minutes)
    end_total_minutes = end_hours * 60 + end_minutes

    travel_minutes = end_total_minutes - start_total_minutes

    if travel_minutes < 0:
        travel_minutes += 1440

    travel_hours = travel_minutes // 60
    travel_minutes = travel_minutes % 60

    return f"{travel_hours:02d}:{travel_minutes:02d}"

