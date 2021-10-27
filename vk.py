import requests
from time import sleep
from tqdm import tqdm

class Vk:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, token, album_id):
        self.album_id = album_id
        self.params = {
            "v": '5.131',
            "access_token": token
        }
        self.id = self._get_user()
        self.result = self._get_photos()

    # Получение идентификатора пользователя
    def _get_user(self):
        print('    Получение числового идентификатора пользователя в системе ВК')
        method = 'users.get'
        url = self.base_url + method
        res = requests.get(url=url, params=self.params)
        id = res.json()['response'][0]['id']
        print(f"    * Идентификатор текущего пользователя: {id}")
        print('')
        return id

    # Получение метаданных фотографий из альбома профиля
    def _get_photos(self):
        method = 'photos.get'
        params_photos = {
            "owner_id": self.id,
            "album_id": self.album_id,
            "extended": 1,
            "photo_sizes": 1
        }
        params = {**self.params, **params_photos}
        url = self.base_url + method
        print('  Получение метаданных фотографий профиля пользователя')
        res = requests.get(url=url, params=params)

        res.raise_for_status()
        result = res.json()['response']['items']
        print('    * Метаданные фотографий профиля пользователя были успешно получены')

        return result

    # Получение словаря с информацией о фотографиях пользователя вк
    def get_photos_metadata(self):
        result = self._get_photos()
        json_dict = []
        likes = []
        # Список лайков по всем фотографиям пользователя
        likes = [photo_info['likes']['count'] for photo_info in result]
        for item in tqdm(result, desc='Анализ метаданных фотографий', bar_format='{l_bar}{bar:50}{r_bar}{bar:-50b}'):
            sleep(.5)
            item_dict = {}
            
            # При наличии дубликата в значении кол-ва лайков у фото к названию добавляется дата фотографии
            if likes.count(item['likes']['count']) > 1:
                item_dict['file_name'] = f"{item['likes']['count']}_{item['date']}.jpg"
            else:
                item_dict['file_name'] = f"{item['likes']['count']}.jpg"

            # Создание списков с информацией о фотографии 
            # для дальнейшего получения ссылки на фотографию с самым большим разрешением
            height_list = []
            type_list = []
            url_list = []
            for photo in item['sizes']:
                height_list.append(photo['height'])
                type_list.append(photo['type'])
                url_list.append(photo['url'])

            # Получение значений типа размера и ссылки на фотографию с данным типом размера 
            # в зависимости от самого большого значения ширины фотографии
            item_dict['size'] = type_list[height_list.index(max(height_list))]
            item_dict['url'] = url_list[height_list.index(max(height_list))]

            json_dict.append(item_dict)

        return json_dict

    
