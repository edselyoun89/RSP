# Лабораторная работа №3 — каркас серверного приложения

## Вариант и результат

Вариант №18: электронная библиотека и каталог книг. Реализован минимальный запускаемый каркас на Python 3.10+ без внешних runtime-зависимостей. Сервер отвечает на:

- `GET /health`
- `GET /api/v1/health`

Оба маршрута используют один и тот же `HealthService`; HTTP-слой не содержит бизнес-правил.

## Структура

```text
lab3/
├── app/
│   ├── main.py                         # точка входа и HTTP-сервер
│   └── internal/
│       ├── config/settings.py          # загрузка .env и типизированные настройки
│       ├── controller/health.py        # HTTP-контроллер health-check
│       ├── domain/models.py             # модели домена и ответа
│       ├── repository/health_repository.py # источник технического состояния
│       └── service/health_service.py    # сценарий проверки здоровья
├── tests/test_health.py                 # автоматические проверки сервиса и HTTP
├── .env.example                         # шаблон конфигурации
├── .gitignore                           # исключает .env и служебные файлы
├── openapi.yaml                         # контракт health endpoint
├── ARCHITECTURE.md                      # описание слоёв и контрольные вопросы
└── pyproject.toml
```

## Запуск

1. Установить Python 3.10 или новее.
2. При необходимости изменить локальный `.env` по шаблону `.env.example`.
3. Запустить из каталога `lab3`:

```powershell
python -m app.main
```

Эта команда занимает текущий терминал и оставляет сервер запущенным. Не закрывайте это окно и не нажимайте `Ctrl+C` до завершения проверки. Для запроса откройте **второе** окно PowerShell в том же каталоге.

Проверить ответ:

```powershell
curl.exe http://127.0.0.1:8080/api/v1/health
```

В Windows команда `curl` иногда является псевдонимом PowerShell для `Invoke-WebRequest`; вариант `curl.exe` явно запускает настоящий curl. Если сервер был остановлен, сначала снова выполните `python -m app.main`.

Ожидаемый JSON:

```json
{
  "status": "pass",
  "app_name": "Library API",
  "version": "1.0.0",
  "environment": "development"
}
```

## Проверка

```powershell
python -m unittest discover -s tests -v
```

Файл `.env` создан только для локального запуска и исключён из Git правилом `.gitignore`; в репозитории должен храниться только [.env.example](./.env.example).
