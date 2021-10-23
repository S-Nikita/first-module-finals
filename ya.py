import requests
import json
import os.path

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
        if path:
            for i, item in enumerate(self.json_dict):
                # photos_count = int(input('Введите кол-во фотографий, которое Вы хотите сохранить на Yandeks Disk: '))
                photos_count = 5
                if photos_count < len(self.json_dict):
                    print('Указанное Вами кол-во фотографий больше имещегося значения, будут загружены все фотографии из альбома')
                    photos_count = len(self.json_dict) + 1
                if i < photos_count:
                    params = {"path": f"/{path}/{item['file_name']}", "url": {item['url']}}
                    res = requests.post(url=url, headers=self.header, params=params)
                    if res.status_code == 202:
                        print(f"    ** Фотография №{i + 1} успешно загружена")
                    else:
                        print(f"    ** Возникла ошибка при загрузке фотографии, код ошибки: {res.status_code}")
            
            photos_metadata = self._create_json(self.json_dict)
            if photos_metadata:
                print('  JSON файл со списком метаданных фотографий успешно создан на диске')
            else:
                print('  При создании JSON файла со списком метаданных фотографий произошла ошибка')
            
            return res
