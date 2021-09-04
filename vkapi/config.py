from os import getenv

token = "98d6ab8c434c696ce884b479963b75bddf9fb3b2366937babfeffcc3dbed3b2c9958349e3a986cd1da9da"

max_photo_save = 10  # ограничение для теста по сохранению картинок, если поставить 0, то ограничения не будет
threads_count = 2  # сколько максимум активных потоков выделяется под джобы


"""
    для винды
        base_domen = "localhost"
        base_port = 27017

    для докера
        base_domen = "mongo"
        base_port = 27017

    имя клиента и имя коллекции настроить под себя
"""
base_domen = "mongo"
base_port = 27017
client_name = "vkmonitor"
default_collection_name = "photos"
jobs_collection_name = "jobs"
