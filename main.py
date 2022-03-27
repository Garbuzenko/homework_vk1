# from chardet.universaldetector import UniversalDetector
# import os
# from pathlib import Path
# import operator
# import time
# from unittest import result
import time
import requests
from pprint import pprint

class Session(object):
    API_URL = 'https://api.vk.com/method/'
    def __init__(self, access_token=None):
        self.access_token = access_token
        # self.requests_session.headers['Accept'] = 'application/json'
        # self.requests_session.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def get_max_url(self, item):
        max_height = -1
        res = ""
        for s in item['sizes']:
            if s['height'] > max_height:
                max_height = s['height']
                res = s['url']
        return res

    def photos_get(self, owner_id:str):
      method = 'photos.get'
      url = self.API_URL + method
      params = {
          'owner_id': owner_id,
          'album_id': 'profile',
          'access_token': self.access_token,
          'extended': 1,
          'v': '5.131'
      }
      # print(params)
      res = requests.get(url, params=params)
      # print(res)
      # print(res.json())
      return res.json()

class YaUploader:
    host = 'https://cloud-api.yandex.net'
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_meta(self, path, only_name=0):
        method = '/v1/disk/resources'
        info = []
        url = self.host + method
        params = {"path": path}
        resp = requests.get(url, headers=self.get_headers(), params=params)
        files = resp.json()['_embedded']['items']
        for f in files:
            if only_name == 0:
                info.append({'name': f['name'], 'size': str(f['size'])})
            else:
                info.append(f['name'])
        return info
    def get_href_for_upload(self, path: str, href=""):
        method = '/v1/disk/resources/upload'
        url = self.host + method
        try:
            if url != '':
                # print(href)
                params = {"path": path, "url": href, "overwrite": "false"}
                resp = requests.post(url, headers=self.get_headers(), params=params)
            else:
                params = {"path": path, "overwrite": "true"}
                resp = requests.get(url, headers=self.get_headers(), params=params)
            # print(resp.json())
            return resp.json()['href']
        except:
            return ""

    def create_dir(self, path):
        method = '/v1/disk/resources'
        url = self.host + method
        params = {"path": path}
        resp = requests.put(url, headers=self.get_headers(), params=params)
        # print(resp.json())

    def upload(self, href: str, upload_file=""):
        if href != "":
            if upload_file != "":
                resp = requests.put(href, headers=self.get_headers(), data=open(upload_file, 'rb'))
            else:
                resp = requests.get(href, headers=self.get_headers())

            resp.raise_for_status()
            return resp.status_code

        else:
            return "Пустой URL"


if __name__ == '__main__':
    global_path = "netology"
    token_vk = ''
    token_yandex = ''

    owner_id = str(input("Введите id пользователя="))
    if token_yandex == "":
        token_yandex = str(input("Введите токен yandex="))
    if token_vk == "":
        token_vk = str(input("Введите токен vk="))

    yandex = YaUploader(token_yandex)
    vk = Session(token_vk)
    photos = vk.photos_get(owner_id)
    if photos.get('error') != None:
        pprint(photos['error']['error_msg'])
    elif photos.get('response') != None:
        items = photos['response']['items']
        owner_dir = global_path + "/" + owner_id
        yandex.create_dir(owner_dir)  # Создадим папку
        info = yandex.get_meta(owner_dir, only_name=1)
        # print(info)
        for item in items:
            file_name = str(item['likes']['count']) + '.jpg'
            if file_name in info:
                print("Файл уже существует")
            else:
                path_to_file = owner_dir + "/" + file_name
                href_file = vk.get_max_url(item) #Получим ссылку с max размером
                href = yandex.get_href_for_upload(path_to_file, href=href_file) #Получим ссылку для загрузки файла
                result = yandex.upload(href=href) #Выполним загрузку
                print(result, path_to_file, href_file)
        time.sleep(1) #Подождем загрузку последнего файла
        info = yandex.get_meta(owner_dir)
        print(info)

        #Создать файл
        with open(owner_id + '.json', mode='w') as new_file:
            new_file.writelines(str(info))



