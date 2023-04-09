# Записи матчей игры Gwent

## Приложение

Приложение представляет собой код на языке программирования Python 
с использованием библиотеки Flask для создания локального сервера, 
файлов html + css + js для обеспечения графического интерфейса пользователя, 
а также базы данных SQLite3 и встроенной библиотеки unittest для 
проведения Unit тестирования.

## Структура

- **static** - статичные (неизменяемые) файлы .js и .css
  - **scripts**
    - *admin.js* - код JavaScript для административного раздела сайта
    - *history.js* - код JS для страницы просмотра деталей конкретного матча
    - *replays.js* - код JS для страницы просмотра списка всех матчей
  - **styles**
    - *admin.css* - стили CSS для административного раздела сайта
    - *game_forms.css* - стили CSS для форм создания/изменения/удаления матчей в административном разделе
    - *history.css* - стили CSS для страницы просмотра деталей конкретного матча 
    - *replays.css* - стили CSS для страницы просмотра списка всех матчей
    - *site.css* - общие для всех страниц стили CSS
- **templates** - файлы .html, выступающие как шаблоны для страниц
  - *admin.html* - страница административного раздела
  - *history.html* - страница просмотра деталей конкретного матча 
  - *index.html* - страница просмотра списка всех матчей
  - *notification.html* - страница уведомления о результате создания/изменения/удаления матча на стороне сервера
- **gen.py** - программа создания тестовой базы данных и её заполнения игроками (может быть запущено несколько раз)
- **gwent_db.sqlite3** - готовая тестовая база данных SQL, созданная с помощью `gen.py` и уже заполненная несколькими записями матчей через административный раздел
- **main.py** - backend сайта, связывает страницы с базами данных
- *objects-template.py* - основы классов `Users` и `Game_records` для лабораторной работы №3 (в программе не используются)
- **objects.py** - написанные классов `Users` и `Game_records`, работают с базой данных
- *requirements.txt* - необходимые внешние библиотеки Python
- *test_db-copy.sqlite3* - база данных, на которой проводятся Unit тесты (резерв)
- **test_db.sqlite3** - база данных, на которой проводятся Unit тесты
- **tests.py** - программа, тестирующая классы из `objects.py` - Unit-тестирование

## Создание тестовой БД для локального сервера

`python ./gen.py` (несколько раз, если нужно больше пользователей)

Либо используйте готовую `gwent_db.sqlite3`

## установка библиотеки flask (для администрации)

`pip install Flask==2.2.2`

## запуск локального сервера

`flask --app main.py run`

Основной раздел сайта: `http://127.0.0.1:5000`

Административный раздел сайта: `http://127.0.0.1:5000/admin`

## Unit-тестирование

`python ./tests.py`
