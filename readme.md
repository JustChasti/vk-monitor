1) Создать env из env.example
2) Зайти в config в vkapi
3) Поставить свой токен приложения, можно этот оставить
4) Снять ограничение по количеству сохраняемых фото поставить 0 (max_photo_save)
5) Поставить максимальное количество одновременно выполняемых потоков для джоб (threads_count)
6) Если надо поменять настройки для mongo - зайти в config в vkapi и flaskapi там все в целом понятно 
(default_collection_name - это куда сохраняются параметры фоток, jobs_collection_name - куда сохраняются параметры джоб)
7) Зайти в servertest и выставить параметры запроса + уникальное имя джобы, запрос должен отправится на flask сервер и сохраниться в базе
