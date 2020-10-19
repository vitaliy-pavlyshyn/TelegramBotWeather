import requests
import json
import time
import const
from pprint import pprint


def emoji_weather_encoding(data):
    if data == 'Clear':
        return '✨'
    elif data == 'Clouds':
        return '☁️'
    elif data == 'Thunderstorm':
        return '⛈️'
    elif data == 'Drizzle':
        return '🌦️'
    elif data == 'Rain':
        return '🌧️'
    elif data == 'Snow':
        return '❄️'
    else:
        return '💨'


def answer_user_bot(user_id, data):
    params = {
        'chat_id': user_id,
        'text': data
    }
    url = const.URL.format(token=const.TOKEN, method=const.SEND_METHOD)
    answer = requests.post(url, params=params)


def parse_weather_data(data):
    current_temperature = data['main']['temp']
    feels_like_temperature = data['main']['feels_like']
    for elem in data['weather']:
        weather_state = elem['main']
        detail_weather = elem['description'].capitalize()
    weather_state = emoji_weather_encoding(weather_state) + detail_weather
    return weather_state, current_temperature, feels_like_temperature


def get_weather(location):
    url = const.WEATHER_URL.format(city=location, token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'City not found!'
    data = json.loads(response.content)
    weather_sum = parse_weather_data(data)
    msg = '{} in {} now. \n It`s {} , but feels like {}.'.format(weather_sum[0], location, weather_sum[1],
                                                                 weather_sum[2])
    print(msg)
    return msg


def get_message(data):
    message = data['message']['text']
    user_id = data['message']['chat']['id']
    return message, user_id


def save_update_id(update):
    with open('update_id', 'w') as file:
        file.write(str(update['update_id']))
    const.UPDATE_ID = update['update_id']
    return True


def main():
    while True:
        url = const.URL.format(token=const.TOKEN, method=const.UPDATE_METHOD)
        content = requests.get(url).text

        data = json.loads(content)

        result = data['result'][::-1]
        needed_part = None
        for elem in result:
            if elem['message']['chat']['id'] == const.MY_ID:
                needed_part = elem
                break

        if const.UPDATE_ID != needed_part['update_id']:
            message, user_id = get_message(needed_part)
            weather = get_weather(message)
            answer_user_bot(user_id, weather)
            save_update_id(needed_part)
            time.sleep(5)


if __name__ == '__main__':
    main()
