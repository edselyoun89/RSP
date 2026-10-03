# Минимальный runtime-образ: приложение не требует компиляции и внешних пакетов.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_NAME="Library API" \
    APP_VERSION=1.0.0 \
    APP_ENV=container \
    HTTP_HOST=0.0.0.0 \
    HTTP_PORT=8080

WORKDIR /app

# В production-контейнер попадает только исполняемый слой приложения.
COPY lab3/app ./app

# Запуск от непривилегированного пользователя.
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/v1/health', timeout=2)"

CMD ["python", "-m", "app.main"]
