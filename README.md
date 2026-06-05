# Анализатор страниц

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Vitaocy/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Vitaocy/python-project-83/actions)
[![Linter check](https://github.com/Vitaocy/python-project-83/actions/workflows/check.yml/badge.svg)](https://github.com/Vitaocy/python-project-83/actions/workflows/check.yml)

### SonarCloud status:
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                           
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                                               
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                                    
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                              
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                                        
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                      
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                            
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                                 
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)                                        
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Vitaocy_python-project-83&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Vitaocy_python-project-83)

Проект доступен по ссылке: https://python-project-83-nvjk.onrender.com

## Описание проекта

Анализатор страниц — это веб-приложение для проверки сайтов на базовую SEO-пригодность.  
Пользователь может добавить сайт, запустить проверку и получить информацию о:

- коде ответа сервера
- содержимом тега `title`
- заголовке `h1`
- мета-описании (`description`)

Приложение хранит историю проверок и позволяет просматривать результаты для каждого добавленного сайта.

Проект разработан на Python с использованием Flask.  
В качестве базы данных используется PostgreSQL.

## Требования

- Python 3.14+
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/Vitaocy/python-project-83.git
cd python-project-83
```

2. Создать `.env` в корне проекта и добавить переменные окружения:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
```

3. Создайте базу данных PostgreSQL:

```bash
createdb db_name
```

4. Установить uv, зависимости, инициализировать базу данных:

```bash
make build
```

## Запуск приложения

В режиме разработки:

```bash
make dev
```

Продакшн-запуск:

```bash
make start
```

По умолчанию запускается на порту `8000`.

Можно указать свой порт:

```bash
make start PORT=1234
```

После запуска приложение будет доступно по адресу:

```
http://127.0.0.1:8000
```