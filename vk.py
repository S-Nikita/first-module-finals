import requests

class Vk:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, token, album_id):
        self.album_id = album_id
        self.token = token
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

        if res.status_code == 200:
            result = res.json()['response']['items']
            print('    * Метаданные фотографий профиля пользователя были успешно получены')
        else:
            result = []
            print('    * Произошла ошибка при получении информации о фотографиях пользователя')
            print(f"    ** Код ошибки: {res.status_code}")
        return result

    # Присваивание названий фотографиям на основе кол-ва лайков и даты загрузки в систему ВК
    def _get_file_name(self):
        # Инициализация необходимых переменных
        likes = []
        dates = []
        json_dict = []
        file_name = ''
        result = self.result

        # Создание списков с кол-вом лайков и дат для каждой из фотографий
        for item in result:
            likes += [item['likes']['count']]
            dates += [item['date']]
        
        # Получение финального названия каждой фотографии
        for i, like in enumerate(likes):
            j = 0
            ## Анализ значений кол-ва лайков у фотографий, если значения не уникальны, 
            ## к итоговому названию добавляется дата загрузки фотографии в систему вк
            while j < len(likes):
                if i != j:
                    if likes[j] == like:
                        file_name = f"{result[i]['likes']['count']}_{result[i]['date']}"
                    else:
                        file_name = str(likes[i])
                j += 1
            file_name += '.jpg'
            json_dict += [{"file_name": file_name}]

        return json_dict

    # Добавление информации о ссылке для скачивания фотографии и ее размере в итоговый словарь
    def get_photos_metadata(self):
        result = self.result
        json_dict = []
        if result:
            json_dict = self._get_file_name()
            for i, item in enumerate(result):
                size_types = []
                max_size = ''
                ## Градация размеров фотографии от большого к меньшему:
                for size in item['sizes']:
                    size_types += size['type']
                if size_types.count('w') > 0:
                    max_size = 'w'
                elif size_types.count('z') > 0:
                    max_size = 'z'
                elif size_types.count('y') > 0:
                    max_size = 'y'
                elif size_types.count('x') > 0:
                    max_size = 'x'
                elif size_types.count('r') > 0:
                    max_size = 'r'
                elif size_types.count('q') > 0:
                    max_size = 'q'
                elif size_types.count('p') > 0:
                    max_size = 'p'
                elif size_types.count('o') > 0:
                    max_size = 'o'
                elif size_types.count('m') > 0:
                    max_size = 'm'
                elif size_types.count('s') > 0:
                    max_size = 's'
                url = item['sizes'][size_types.index(max_size)]['url']
                
                json_dict[i]["size"] = max_size
                json_dict[i]["url"] = url

        return json_dict

    
