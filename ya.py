import requests
import json
import os.path

from requests.api import head

class Ya:
    def __init__(self, token, json_dict):
        self.token = token
        self.json_dict = json_dict
        self.header = self._get_header()

    # Получение необходимых параметров для header
    def _get_header(self):
        header = {
            "Content-Type": 'aplication/json',
            "Authorization": 'OAuth {}'.format(self.token)
        }

        return header

    # Создание папки в которую будут загружаться фотографии
    def _create_folder(self):
        header = self.header
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        params = {"path": 'VK_PICTURES'}
        print('  Создание папки в которую будут загружаться фотографии')
        res = requests.put(url=url, headers=header, params=params)

        if res.status_code == 201 or res.status_code == 409:
            print(f"    * Папка с названием {params['path']} создана на диске")
            path = params['path']
        else:
            path = ''
            print("    * Не удалось создать папку на диске, код ошибки: {res.status_code}")

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

    # Получение ссылки для загрузки локального файла
    def _get_upload_link(self, url, path_to_upload):
        params = {"path": f"{path_to_upload}/photos_metadta.json", "overwrite": "true"}
        print(path_to_upload)
        res = requests.get(url=url, headers=self.header, params=params)
        
        if res.status_code == 200:
            url = res.json()['href']
        else:
            url = ''

        return url


    def upload_to_ya(self):
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        path = self._create_folder()
        if path:
            for i, item in enumerate(self.json_dict):
                params = {"path": f"/{path}/{item['file_name']}", "url": {item['url']}}
                res = requests.post(url=url, headers=self.header, params=params)
                if res.status_code == 202:
                    print(f"    ** Фотография №{i + 1} успешно загружена")
                else:
                    print(f"    ** Возникла ошибка при загрузке фотографии, код ошибки: {res.status_code}")

            photos_metadata = self._create_json(self.json_dict)
            if photos_metadata:
                href  = self._get_upload_link(url, path)
                print(href)
                res = requests.put(url=href, data=open('photos_metadta.json', 'rb'))
                res.raise_for_status()
                return res.status_code
