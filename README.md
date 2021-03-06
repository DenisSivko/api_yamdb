# Групповой проект «Yamdb»
## Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок высчитывается средняя оценка произведения.
##### Функционал:
###### REVIEWS
- Получить список всех отзывов
- Создать новый отзыв
- Получить отзыв по id
- Частично обновить отзыв по id
- Удалить отзыв по id
###### COMMENTS
- Получить список всех комментариев к отзыву по id
- Создать новый комментарий для отзыва
- Получить комментарий для отзыва по id
- Частично обновить комментарий к отзыву по id
- Удалить комментарий к отзыву по id
###### AUTH
- Отправление confirmation_code на переданный email
- Получение JWT-токена в обмен на email и confirmation_code
###### USERS
- Получить список всех пользователей
- Создание пользователя
- Получить пользователя по username
- Изменить данные пользователя по username
- Удалить пользователя по username
- Получить данные своей учетной записи
- Изменить данные своей учетной записи
###### CATEGORIES
- Получить список всех категорий
- Создать категорию
- Удалить категорию
###### GENRES
- Получить список всех жанров
- Создать жанр
- Удалить жанр
###### TITLES
- Получить список всех объектов
- Создать произведение для отзывов
- Информация об объекте
- Обновить информацию об объекте
- Удалить произведение

Документация к API доступна по адресу `http://127.0.0.1:8000/redoc/`
## Установка
Клонируем репозиторий на локальную машину:

git clone `https://github.com/DenisSivko/api_yamdb.git`

Создаем виртуальное окружение:

`python -m venv venv`

Устанавливаем зависимости:

`pip install -r requirements.txt`

Применяем миграции:

`python manage.py migrate`

Запуск:

`python manage.py runserver`

## Примеры
##### Получаем confirmation_code
Для формирования запросов и ответов использована программа [Postman](https://www.postman.com/).

Отправляем POST-запрос на адрес `http://127.0.0.1:8000/api/v1/auth/email/` 

- Обязательное поле: `email`

![token_image](https://i.ibb.co/wYVTNLC/email.png)

Код подтверждения будет доступен по адресу `api_yamdb\sent_emails\file.log`

##### Получаем token
Отправляем POST-запрос для получения JWT-токена на адрес `http://127.0.0.1:8000/api/v1/auth/token/`.
- Обязательное поле: `email`,
- Обязательное поле: `confirmation_code`

![posts_image](https://i.ibb.co/FJ9bZvJ/token.png)
