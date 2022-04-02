import requests


class VkClass(object):
    API_URL = 'https://api.vk.com/method/'

    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_id(self, user_ids):
        method = 'users.get'
        url = self.API_URL + method
        params = {
            'user_ids': user_ids,
            'access_token': self.access_token,
            'v': '5.131'
        }
        res = requests.get(url, params=params)
        response = res.json().get("response")
        _id = 0
        for r in response:
            _id = r.get("id")
            break
        return _id

    @staticmethod
    def get_max_url(item):
        max_height = -1
        res = ""
        for s in item['sizes']:
            if s['height'] > max_height:
                max_height = s['height']
                res = s['url']
        return res

    def photos_get(self, owner_id: str, count=5):
        method = 'photos.get'
        url = self.API_URL + method
        params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'access_token': self.access_token,
            'extended': 1,
            'count': count,
            'v': '5.131'
        }
        res = requests.get(url, params=params).json()

        if res.get('error') is not None:
            print(res['error']['error_msg'])

        return res
