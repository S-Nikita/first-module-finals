import requests
import json
import os.path
from time import sleep
from tqdm import tqdm

from requests.api import head

class Ya:
    def __init__(self, token, json_dict):
        self.json_dict = json_dict
        self.header = {
            "Content-Type": 'aplication/json',
            "Authorization": 'OAuth {}'.format(token)
        }

    # Создание папки в которую будут загружаться фотографии
    def _create_folder(self):
        header = self.header
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        params = {"path": 'VK_PICTURES'}
        print('  Создание папки в которую будут загружаться фотографии')
        res = requests.put(url=url, headers=header, params=params)

        res.raise_for_status()
        print(f"    * Папка с названием {params['path']} создана на диске")
        print('')
        path = params['path']

        return path

    # Создание json файла
    def _create_json(self, json_dict):
        ## Приводим словарь к финальному виду удаляя ключ "url" с его значением
        for item in json_dict:
            item.pop('url')

        ## Создаем файл в формате json на основе полученного словаря
        with open('photos_metadta.json', 'w') as f:
            json.dump(json_dict, f, ensure_ascii=False, indent=2)

        return os.path.exists('photos_metadta.json')

    def upload_to_ya(self):
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        path = self._create_folder()

        photos_count = 5
        photos_count = min(photos_count, len(self.json_dict))
        for item in tqdm(self.json_dict[:photos_count], desc='Загрузка фотографий', bar_format='{l_bar}{bar:50}{r_bar}{bar:-50b}'):
            sleep(.5)
            params = {"path": f"/{path}/{item['file_name']}", "url": {item['url']}}
            res = requests.post(url=url, headers=self.header, params=params)
            res.raise_for_status()
            print('')
            
        photos_metadata = self._create_json(self.json_dict)
        if photos_metadata:
            print('  JSON файл со списком метаданных фотографий успешно создан на диске')
        else:
            print('  При создании JSON файла со списком метаданных фотографий произошла ошибка')
