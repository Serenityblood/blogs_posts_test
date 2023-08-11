# blogs_posts_test
Сервис для написания постов в личных блогах пользователей

## Стэк:
```
Django, DRF, PostgreSQL, Celery, Redis, Docker
```

## Установка:

1. В корневой папке проекта:
```
Создать .env файл по примеру env.example
```
```
docker-compose up -d --build
```
2. Создать суперюзера(обязательно для дальнейшего шага)
```
docker-compose exec web python manage.py createsuperuser
```
3. Заполнить базу данных:
```
docker-compose exec web python manage.py add_data
```

## Эндпоинты:
1. http://127.0.0.1:8000/api/users/
Регистрация
>Request sample:
```
{
    'username': string,
    'password': string
}
```
2. http://127.0.0.1:8000/auth/jwt/create/
Получение токена
>Request sample:
```
{
    'username': string,
    'password': string
}
```
>Response sample:
```
{
    'resfresh': token,
    'access': token,
}
```
Header - Bearer
3. http://127.0.0.1:8000/api/posts/
Получение, создание постов
>Request sample:
```
{
    'title': string,
    'text': string
}
```
4. http://127.0.0.1:8000/api/blogs/{id}
Подписаться на блог с {id}

3. http://127.0.0.1:8000/api/users/postsfeed/
Генерация ленты постов на основе подписок пользователя с пагинацией по 10 постов
