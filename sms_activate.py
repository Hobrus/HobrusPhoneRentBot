import requests
import json


def get_phone_number(api_key, service='tg', country=6):
    base_url = 'https://sms-activate.ru/stubs/handler_api.php'
    params = {
        'api_key': api_key,
        'action': 'getNumberV2',
        'service': service,
        'country': country,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data['phoneNumber'], data['activationId']  # Возвращаем номер телефона и ID активации
    else:
        print("Error: ", response.status_code)
        return "Error: " + str(response.status_code), None


def set_status(api_key, id, status):
    base_url = 'https://sms-activate.ru/stubs/handler_api.php'
    params = {
        'api_key': api_key,
        'action': 'setStatus',
        'status': status,
        'id': id,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return "Error: " + str(response.status_code)


def get_status(api_key, id):
    base_url = 'https://sms-activate.ru/stubs/handler_api.php'
    params = {
        'api_key': api_key,
        'action': 'getStatus',
        'id': id,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return "Error: " + str(response.status_code)
