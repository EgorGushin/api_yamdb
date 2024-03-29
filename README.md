# API YaMDb
## Описание проекта:

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Список категорий (Category) может быть расширен (например, можно добавить 
категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм 
или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, 
в категории «Книги» могут быть произведения «Винни Пух и все-все-все» 
и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы 
«Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из 
списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые 
отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от 
одного до десяти). Из множества оценок автоматически высчитывается 
средняя оценка произведения.

Полная документация к API находится в /redoc

## Технологии:
- Python 3.7, Django 2.2, DRF, JWT

<details>
<summary><h2>Как запустить проект:</h2></summary>

### *Клонировать репозиторий:*
```
git clone https://github.com/UnRainbow/api_yamdb.git
```

### *Cоздать и активировать виртуальное окружение:*
```
python3 -m venv venv
source venv/Scripts/activate
```

### *Установить зависимости из файла requirements.txt:*
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### *Выполнить миграции:*
```
python3 manage.py makemigrations
python3 manage.py migrate
```

### *Запустить проект:*
```
python3 manage.py runserver
```

## База данных:

В репозитории в директории /api_yamdb/static/data, подготовлены несколько 
файлов в формате csv с контентом для ресурсов 
Users, Titles, Categories, Genres, Review и Comments.

### ***Для загрузки данных, получаемых вместе с проектом:***

### *Установите библиотеку pandas*
```
pip install pandas
```

### *Запустите management-команду, добавляющую данные в БД через Django ORM*
```
python3 manage.py import_csv
```
</details>

## Команда разработки:
- [Первухина Анна](https://github.com/pervukhina-anna) - управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail.
- [Гущин Егор](https://github.com/EgorGushin) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них.
- [Деревянченко Сергей](https://github.com/Sergey-Derevyanchenko) - отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений.
