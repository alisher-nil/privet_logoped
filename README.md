
![Static Badge](https://img.shields.io/badge/python-1c4161?logo=python&logoColor=3776AB)
![Static Badge](https://img.shields.io/badge/django-4.2-Grey?style=flat&logo=django&logoColor=%23092E20)
![Static Badge](https://img.shields.io/badge/aiogram-3.10-blue?style=flat)
![Static Badge](https://img.shields.io/badge/vkbottle-4.3-blue?style=flat)
![Static Badge](https://img.shields.io/badge/docker-white?style=flat&logo=docker&logoColor=%232496ED)

# Описание
Боты для телеграма и вк с бэкендом на DRF в рамках хакатона для проекта Привет-логопед.

# Задачи
## Сделано
- Взаимодействие ботов с бэкендом через API
- Настраиваемое меню
- Управления ролями пользователей
- Вопросы логопеду/администратору и ответы на них
## Не сделано
- Авторизация в API
- Настройка текстов главного меню
- Подписка/отписка на напоминания
- Тесты
- Подписка/отписка на рассылку
- Интерфейс в админке для ответов на вопросы
- Менеджмент пользователей (Троттлинг вопросов, баны)
# Запуск 
## Запуск компонентов по отдельности
### Пререквезиты
- python
- docker
### Пошаговые действия
- Склонируйте репозиторий
```bash
git clone https://github.com/Studio-Yandex-Practicum/Privet_Logoped_team_2.git
```
#### Бэкенд Django
Перейдите в каталог бэкенда
```bash
cd django_app
```
- Создайте виртуальное окружение
```bash
python -m venv .venv
```
- Активируйте виртуальное окружение
```
source .venv/Scripts/activate
```
- Обновите pip
```bash
python -m pip install --upgrade pip
```
- Установите зависимости
```bash
pip install -r requirements.txt
```
- Создайте `.env` файл. `.env.example` доступен для примера.
- Для запуска бэкенда нужен сервер postgresql, если его нет, в каталоге docker есть конфигурация докера для запуска контейнера только с postgresql и настройками необходимыми для подключения. На этом этапе - подходящий момент чтобы его запустить.
```bash
cd docker
docker-compose -f docker-compose.db_dev.yml up --build -d
```
Перейдите в каталог приложения django:
```
cd privet_logoped
```
- Примените миграции
```bash
python manage.py migrate
```
- Создайте суперпользователя
```bash
python manage.py createsuperuser
```
- Запустите приложение
```bash
python manage.py runserver
```
#### Бот Telegram
Перейдите в каталог бота
```bash
cd telegram_bot
```
- Создайте виртуальное окружение
```bash
python -m venv .venv
```
- Активируйте виртуальное окружение
```
source .venv/Scripts/activate
```
- Обновите pip
```bash
python -m pip install --upgrade pip
```
- Установите зависимости
```bash
pip install -r requirements.txt
```
- Запустите бота
```bash
python main.py
```
#### Бот ВК
Перейдите в каталог бота
```bash
cd vk_bot
```
- Создайте виртуальное окружение
```bash
python -m venv .venv
```
- Активируйте виртуальное окружение
```
source .venv/Scripts/activate
```
- Обновите pip
```bash
python -m pip install --upgrade pip
```
- Установите зависимости
```bash
pip install -r requirements.txt
```
- Перейдите в каталог приложения
```bash
cd src
```
- Запустите бота
```bash
python main.py
```
## Запуск в контейнерах
В каталоге докер есть настроенная конфигурация docker-compose для запуска всей связки приложений в контейнерах.
- Перейдите в каталог docker
```bash
cd docker
```
- Создайте .env файл
- Запустите контейнеры
```bash
docker-compose up --build -d
```
Примените миграции
```bash
docker-compose exec backend python manage.py migrate
```
- Создайте суперпользователя
```bash
docker-compose exec backend python manage.py createsuperuser
```