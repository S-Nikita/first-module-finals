from vk import Vk
from ya import Ya

if __name__ == '__main__':
    token_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    album_id = 'profile'

    token_ya = 'TOKEN_PLACEHOLDER'

    print('Запуск программы')
    print('#########################################################')
    photos = Vk(token_vk, album_id)
    json_dict = photos.get_photos_metadata()

    if json_dict:
        uploader = Ya(token_ya, json_dict)
        response_status = uploader.upload_to_ya()
        if response_status == 200 or response_status == 201:
            print('  Все необходимые файлы были загружены')
            print('#########################################################')
            print('Выполнение программы завершено успешно')
        else:
            print('  Процесс загрузки файлов завершен с ошибкой, код: ', response_status)
            print('#########################################################')
            print('Выполнение программы завершено c ошибкой')
    else:
        print('#########################################################')
        print('Выполнение программы остановлено, процесс был завершен с ошибкой: Ошибка при получении данных из социальной сети')