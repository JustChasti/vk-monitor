token = ("98d6ab8c434c696ce884b479963b75bddf9fb3b2366"
         "937babfeffcc3dbed3b2c9958349e3a986cd1da9da")
q = 'Москва'  # не писать хэштеги, на них пойдут шмотки всякие
lat = 55.755865
longg = 37.617520
begin_time = 1420074061
radius = 100

max_photo_save = 10  # ограничение для тестов

"""
    для винды
        base_domen = "localhost"
        base_port = 27017

    для докера
        base_domen = "mongo"
        base_port = 27017
"""
base_domen = "mongo"
base_port = 27017
client_name = "vkmonitor"
default_collection_name = "photos"
