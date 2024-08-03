# Общее

Проект представляет собой онлайн-сервис, демонстрирующий возможности Django.
Он обладает следующими техническими особенностями:

- В рамках проекта применяется `Django 5`, совместимость с `Python` начиная с версии `3.10`

- В файле `settings.py` определяются переменные среды, а для их конфигурации используется файл `.env`

- `DEBUG = True` в файле `.env` запускает проект в **режиме разработки**

- `DEBUG = False` в файле `.env` либо отсутствие `DEBUG` в  файле `.env` запускает проект в **режим эксплуатации**
-
- Чтобы запустить среду в **режиме разработки** с базой данной [PostgreSQL](https://www.postgresql.org/),
необходимо указать в  файле `.env` переменный `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
и соответствующие ему переменные `DJANGO_POSTGRES_HOST`, `DJANGO_POSTGRES_DB`. `DJANGO_POSTGRES_USER` и
`DJANGO_POSTGRES_PASSWORD` в  файле `.env`

# Быстрый старт

## Запустить проект можно с помощью [docker-compose](https://docs.docker.com/compose/install/)

  ```shell
  mv .env.example .env

  docker-compose up -d --build
  ```

## Либо с помощью [Poetry](https://python-poetry.org/).
После установки соответствующего программного обеспечения выполните указанные команды:

- Перенести нужные файлы в рабочую директорию и перейти в рабочий каталог

  ```shell
  mv pyproject.toml ./app/pyproject.toml

  mv .env.example ./app/.env

  cd ./app
  ```

- Настроить среду разработки

  ```shell
  poetry install
  ```
- Создать все таблицы командами

  ```shell
  python manage.py makemigrations store
  python manage.py migrate
  ```

- Создать суперпользователя для доступа к административной панели

  ```shell
  python manage.py ensure_adminuser --no-input
  ```

- Запустить сервер в режиме разработки:

  ```shell
  python manage.py runserver
  ```

Администрирование базы данных происходит через панель управления по адресу http://localhost:8000/admin.
Для авторизации используйте предварительно созданные данные суперпользователя.

# Проверка кода

* [pre-commit](https://github.com/pre-commit/pre-commit-hooks)
  основной пакет проверок

* [black](https://github.com/psf/black)
  форматирует код

* [pyupgrade](https://github.com/asottile/pyupgrade)
  приводит код к последней версии

* [bandit](https://github.com/pycqa/bandit)
  поиск распространенных проблем безопасности в Python

* [isort](https://github.com/pycqa/isort)
  сортирует импорты

* [django-upgrade](https://github.com/adamchainz/django-upgrade)
  Автоматически обновляйте код проекта Django

* [djLint](https://github.com/Riverside-Healthcare/djLint)
  Проверка и форматирование html-шаблонов

* [flake8](https://github.com/PyCQA/flake8)
линтеры, конфигурируется с помощью [.flake8](.flake8)

  * [flake8-commas](https://github.com/PyCQA/flake8-commas)
  улучшает размещения запятых

  * [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)
  находит ошибки и проблемы дизайна в программе

  * flake8-print
  находит `print()` в файлах Python

  * flake8-simplify
  помогает упростить код

  * flake8-annotations-coverage
  обнаруживает отсутствие аннотаций
