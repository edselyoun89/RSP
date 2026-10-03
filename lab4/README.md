# Лабораторная работа №4 — контейнеризация Library API

## Результат

ЛР4 продолжает проект из ЛР1–ЛР3. Уже реализованный Python-каркас из `lab3/` упаковывается в Docker-образ и запускается как изолированный контейнер.

Файлы реализации находятся в корне проекта:

- [Dockerfile](../Dockerfile) — production-образ Python 3.12 Slim;
- [.dockerignore](../.dockerignore) — минимальный build context;
- [app/main.py](../lab3/app/main.py) — точка входа приложения;
- [ARCHITECTURE.md](./ARCHITECTURE.md) — описание решения и ответы на контрольные вопросы.

## Сборка

Из корня репозитория `RSP`:

```powershell
docker build -t rsp-library-api:lab4 .
docker images rsp-library-api
```

`.dockerignore` исключает Git-историю, локальный `.env`, тесты, скриншоты лабораторных и кэши Python. В образ копируется только каталог `lab3/app`.

## Запуск

```powershell
docker run --name rsp-library-container -d `
  -p 8080:8080 `
  -e APP_NAME="Library API" `
  -e APP_VERSION="1.0.0" `
  -e APP_ENV="container" `
  -e HTTP_PORT="8080" `
  rsp-library-api:lab4
```

`HTTP_HOST=0.0.0.0` задан в Dockerfile, поэтому приложение принимает соединения через опубликованный порт контейнера. Конфигурация передаётся через `-e`, а секреты не копируются в образ.

## Проверка

```powershell
curl.exe http://127.0.0.1:8080/api/v1/health
docker ps
docker inspect --format='{{json .State.Health}}' rsp-library-container
docker logs rsp-library-container
```

Ожидаемый ответ:

```json
{
  "status": "pass",
  "app_name": "Library API",
  "version": "1.0.0",
  "environment": "container"
}
```

После демонстрации контейнер останавливается и удаляется:

```powershell
docker stop rsp-library-container
docker rm rsp-library-container
```

## Git

Работа выполняется в ветке `lab4-docker` от актуального `main` и после проверки отправляется в GitHub:

```powershell
git add Dockerfile .dockerignore lab4 README.md
git commit -m "feat(lab4): containerize library API"
git push -u origin lab4-docker
```
