import requests
from vk import Vk
from ya import Ya

if __name__ == '__main__':
    user_id = input('Введите идентификатор пользователя: ')
    token_vk = input('Введите значение токена для API VK: ')
    album_id = input('Введите название альбома, для скачивания фото пользователя ВК(profile, wall, saved): ')

    print('Запуск программы')
    print('#########################################################')
    photos = Vk(token_vk, album_id)
    json_dict = photos.get_photos_metadata()

    if json_dict:
        token_ya = input('Введите значение токена для API Yandex: ')
        
        uploader = Ya(token_ya, json_dict)
        uploader.upload_to_ya()
        print('  Все необходимые файлы были загружены')
        print('#########################################################')
        print('Выполнение программы завершено успешно')
    else:
        print('#########################################################')
        print('Выполнение программы остановлено, процесс был завершен с ошибкой: Ошибка при получении данных из социальной сети')