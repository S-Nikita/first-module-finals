import requests

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

        for item in result:
            item_dict = {}
            # Список лайков по всем фотографиям пользователя
            likes = [photo_info['likes']['count'] for photo_info in result]

            # При наличии дубликата в значении кол-ва лайков у фото к названию добавляется дата фотографии
            if likes.count(item['likes']['count']) > 1:
                item_dict['file_name'] = f"{item['likes']['count']}_{item['date']}.jpg"
            else:
                item_dict['file_name'] = f"{item['likes']['count']}.jpg"

            # Создание списков с информацией о фотографии 
            # для дальнейшего получения ссылки на фотографию с самым большим разрешением
            width_list = [photo['width'] for photo in item['sizes']]
            type_list = [photo['type'] for photo in item['sizes']]
            url_list = [photo['url'] for photo in item['sizes']]

            # Получение значений типа размера и ссылки на фотографию с данным типом размера 
            # в зависимости от самого большого значения ширины фотографии
            item_dict['size'] = type_list[width_list.index(max(width_list))]
            item_dict['url'] = url_list[width_list.index(max(width_list))]

            json_dict += [item_dict]

        return json_dict

    
