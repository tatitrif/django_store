# Общее

Проект представляет собой онлайн-сервис, демонстрирующий возможности Django.
Он обладает следующими техническими особенностями:

- В рамках проекта применяется `Django 5`, совместимость с `Python` начиная с версии `3.10`

- В файле `settings.py` определяются переменные среды, а для их конфигурации используется файл `.env`

  - `DEBUG = True` в файле `.env` запускает проект в **режиме разработки** (с дебаггером)

  - `DEBUG = False` в файле `.env` (либо его отсутствие) запускает проект в **режим эксплуатации**


# Быстрый старт

## Запускаем в **режим эксплуатации**  проект с помощью [docker-compose](https://docs.docker.com/compose/install/)

1.  Чтобы запустить среду с базой данной [SQLite](https://www.sqlite.org/)

  ```shell
  mv .env.example .env

  docker-compose up -d --build
  ```

2.  Чтобы запустить среду с базой данной [PostgreSQL](https://www.postgresql.org/)

  ```shell
  mv .env.example .env

  docker-compose -f docker-compose.yml -f docker-compose-prod.yml  up -d --build
  ```


Панель администратора приложения находится по адресу http://localhost:80/admin.
Для авторизации используйте предварительно созданные данные суперпользователя (из `.env`).

# Проверка кода

* [pre-commit](https://github.com/pre-commit/pre-commit-hooks)
  основной пакет проверок

* [black](https://github.com/psf/black)
  форматирует код

* [pyupgrade](https://github.com/asottile/pyupgrade)
  приводит код к последней версии

* [bandit](https://github.com/pycqa/bandit)
  поиск распространенных проблем безопасности в Python

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
