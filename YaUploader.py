import requests


class YaClass:
    host = 'https://cloud-api.yandex.net'

    def __init__(self, token: str, global_path: str):
        self.token = token
        self.global_path = global_path + "/"
        self.create_dir("")

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_meta(self, path, only_name=0):
        method = '/v1/disk/resources'
        info = []
        path = self.global_path + path
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
        path = self.global_path + path
        url = self.host + method
        # try:
        if url != '':
            params = {"path": path, "url": href, "overwrite": "false"}
            resp = requests.post(url, headers=self.get_headers(), params=params)
        else:
            params = {"path": path, "overwrite": "true"}
            resp = requests.get(url, headers=self.get_headers(), params=params)
        return resp.json()['href']
        # except:
        #     return ""

    def create_dir(self, path):
        method = '/v1/disk/resources'
        url = self.host + method
        path = self.global_path + path
        params = {"path": path}
        requests.put(url, headers=self.get_headers(), params=params)

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
