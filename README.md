Ссылка на сайт:
https://cookfoodgran.zapto.org/

Email и пароль для админки:
Email: admin@mail.ru
Пароль: password

### Описание
«Фудграм» — это сайт, на котором можно публиковать собственные рецепты, добавлять чужие рецепты в избранное, подписываться на других авторов и создавать список покупок для заданных блюд.

### Стек технологий
- Django Rest Framework
- Djoser
- Docker
- PostgreSQL
- Nginx

### Запуск приложения

Создайте директорию для приложения:
```
mkdir foodgram/infra
```
В папку infra скопируйте файлы docker-compose.yml, nginx.conf.
Там же создайте файл .env со следующими переменными:
```
SECRET_KEY=... # секретный ключ django-проекта
DEBUG=False
ALLOWED_HOSTS=... # IP/домен хоста
DB_ENGINE=django.db.backends.postgresql # работаем с БД postgresql
DB_NAME=db.postgres # имя БД
POSTGRES_USER=... # имя пользователя БД
POSTGRES_PASSWORD=... # пароль от БД
DB_HOST=db
DB_PORT=5432
```

Поднимите контейнеры:
sudo docker compose up
В новом окне терминала создайте суперпользователя:
```
docker compose exec backend python manage.py createsuperuser
```
Заполните базу ингридиентами:
```
sudo docker compose exec backend python manage.py loadingredients
```
Соберите статику:
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

### Примеры запросов

Получение списка рецептов:
GET */api/recipes/*
response
```
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/recipes/?page=2",
  "previous": "http://127.0.0.1:8000/api/recipes/?page=1",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "green",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "ya@ya.ru",
        "id": 0,
        "username": "user",
        "first_name": "Ivan",
        "last_name": "Zivan",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Курица",
          "measurement_unit": "г",
          "amount": 100
        }
      ],
      "is_favorited": false,
      "is_in_shopping_cart": false,
      "name": "string",
      "image": "https://backend:8080/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 10
    }
  ]
}
```
Регистрация пользователя:
POST */api/users/*
response
```
{
  "email": "ya@ya.ru",
  "username": "user",
  "first_name": "Ivan",
  "last_name": "Zivan",
  "password": "super_password1"
}
```
response
```
{
  "email": "ya@ya.ru",
  "id": 0,
  "username": "user",
  "first_name": "Ivan",
  "last_name": "Zivan"
}
```
Подписаться на пользователя:
POST */api/users/{id}/subscribe/*
response
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "user",
  "first_name": "Ivan",
  "last_name": "Zivan",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "https://backend:8080/media/recipes/images/image.jpeg",
      "cooking_time": 10
    }
  ],
  "recipes_count": 1
}
```
### Автор
Андрей Логвинов https://github.com/Randy-Colt

