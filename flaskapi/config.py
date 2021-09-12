from os import getenv
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
default_collection_name = getenv('jobscollection')
photos_collection = getenv('defaultcollection')
