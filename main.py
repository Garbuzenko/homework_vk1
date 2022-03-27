import time
from tqdm import tqdm
import requests
from pprint import pprint
import json

class Session(object):
    API_URL = 'https://api.vk.com/method/'
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_max_url(self, item):
        max_height = -1
        res = ""
        for s in item['sizes']:
            if s['height'] > max_height:
                max_height = s['height']
                res = s['url']
        return res

    def photos_get(self, owner_id:str, count=5):
      method = 'photos.get'
      url = self.API_URL + method
      params = {
          'owner_id': owner_id,
          'album_id': 'profile',
          'access_token': self.access_token,
          'extended': 1,
          'count': str(count),
          'v': '5.131'
      }
      res = requests.get(url, params=params)
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

    with open('D:/token.json') as f:
        token_json = json.load(f)
        token_vk = token_json['token_vk']
        token_ya = token_json['token_ya']

    owner_id = str(input("Введите id пользователя="))
    if token_ya == "":
        token_ya = str(input("Введите токен yandex="))
    if token_vk == "":
        token_vk = str(input("Введите токен vk="))

    ya = YaUploader(token_ya)
    vk = Session(token_vk)
    photos = vk.photos_get(owner_id, 10)


    if photos.get('error') != None:
        pprint(photos['error']['error_msg'])
    elif photos.get('response') != None:
        items = photos['response']['items']
        owner_dir = global_path + "/" + owner_id
        ya.create_dir(owner_dir)  # Создадим папку
        info = ya.get_meta(owner_dir, only_name=1)
        for item in tqdm(items):
            file_name = str(item['likes']['count']) + '.jpg'
            if not file_name in info:
                path_to_file = owner_dir + "/" + file_name
                href_file = vk.get_max_url(item) #Получим ссылку с max размером
                href = ya.get_href_for_upload(path_to_file, href=href_file) #Получим ссылку для загрузки файла
                result = ya.upload(href=href) #Выполним загрузку
                # print(result, path_to_file, href_file)
        time.sleep(1) #Подождем загрузку последнего файла
        info = ya.get_meta(owner_dir)
        pprint(info)

        #Создать файл
        with open(owner_id + '.json', mode='w') as new_file:
            new_file.writelines(str(info))




