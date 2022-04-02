import time
from datetime import date
from tqdm import tqdm
from pprint import pprint
import VkSession
import YaUploader
import input_utils

if __name__ == '__main__':
    [token_ya, token_vk] = input_utils.get_tokens()
    ya = YaUploader.YaClass(token_ya, "netology")
    vk = VkSession.VkClass(token_vk)

    owner_id = input_utils.input_owner_id(vk)
    count_photo = input_utils.input_count_photo()

    photos = vk.photos_get(owner_id, count_photo)

    if photos.get('response') is not None:
        items = photos['response']['items']
        owner_dir = str(owner_id)
        ya.create_dir(owner_dir)
        info = ya.get_meta(owner_dir, only_name=1)
        file_name_list = []

        for item in tqdm(items):
            file_name = str(item['likes']['count']) + '.jpg'
            if file_name in file_name_list:
                file_name = str(item['likes']['count']) + str(
                    date.today()) + '.jpg'  # Если кол-во лайков совпало - добавим дату
            if file_name not in info:
                path_to_file = "{0}/{1}".format(owner_dir, file_name)
                href_file = vk.get_max_url(item)  # Получим ссылку с max размером
                href = ya.get_href_for_upload(path_to_file, href=href_file)  # Получим ссылку для загрузки файла
                result = ya.upload(href=href)  # Выполним загрузку
                file_name_list.append("file_name")  # Обработанные

        time.sleep(1)  # Подождем загрузку последнего файла
        info = ya.get_meta(owner_dir)
        pprint(info)

        # Создать файл
        with open(str(owner_id) + '.json', mode='w') as new_file:
            new_file.writelines(str(info))
