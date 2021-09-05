from os import getenv

token = getenv('token')

max_photo_save = int(getenv('maxphotosave')) # ограничение для теста по сохранению картинок, если поставить 0, то ограничения не будет
threads_count = int(getenv('threadscount'))  # сколько максимум активных потоков выделяется под джобы


"""
    Настройки для базы
    для винды
        base_domen = "localhost"
        base_port = 27017

    для докера
        base_domen = "mongo"
        base_port = 27017

    имя клиента и имя коллекции настроить под себя
"""
base_domen = getenv('basedomen')
base_port = int(getenv('port'))
client_name = getenv('client')
default_collection_name = getenv('defaultcollection')
jobs_collection_name = getenv('jobscollection')
