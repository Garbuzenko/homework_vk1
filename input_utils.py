import json


def get_tokens():
    with open('D:/token.json') as f:
        token_json = json.load(f)
        _token_vk = token_json['token_vk']
        _token_ya = token_json['token_ya']
        _token_gd = token_json['token_google_drive']

    if _token_ya == "":
        _token_ya = input("Введите токен yandex=")

    if _token_vk == "":
        _token_vk = input("Введите токен vk=")

    if _token_gd == "":
        _token_gd = input("Введите токен google_drive=")

    return [_token_ya, _token_vk]


def input_owner_id(_vk):
    _id = 0
    while _id < 1:
        _id = _vk.get_id(input("Введите id пользователя или screen_name="))
    return _id


def input_count_photo():
    _count = 0
    while _count < 1:
        try:
            _count = int(input("Введите количество фото="))
        except ValueError:
            print("Введите целое число")
    return _count
