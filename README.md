# Серверное приложение «Электронная библиотека и каталог книг»

Единый Git-репозиторий лабораторных работ по разработке серверных приложений. Индивидуальный вариант — **№18**: читатель, библиотекарь, каталог книг, физические экземпляры, выдача, возврат, бронирование и штрафы.

| Работа | Результат |
|---|---|
| [ЛР1 — архитектура и ERD](./lab1/) | Use Cases, C4 Container, ERD в 3НФ, PostgreSQL DDL |
| [ЛР2 — REST API и OpenAPI](./lab2/) | таблица endpoint’ов, OpenAPI 3.0.3, схемы запросов/ответов, контрольные вопросы |
| [ЛР3 — каркас приложения](./lab3/) | layered-структура, `.env`, health-check, тесты и OpenAPI |
| [ЛР4](./lab4/) | материалы следующего задания, реализация будет добавлена позже |

Текущая ветка `main` содержит завершённые ЛР1–ЛР3 последовательно. Каждая следующая лабораторная добавляется поверх предыдущей отдельным коммитом или веткой.

## Рабочий Git-процесс

```powershell
git switch main
git pull --ff-only origin main
git switch -c lab4-docker
```

После выполнения новой работы:

```powershell
git add lab4
git commit -m "feat(lab4): containerize library API"
git push -u origin lab4-docker
```

Для сдачи через Pull Request ветка сохраняет историю прошлых лабораторных. Для линейного варианта её можно слить в `main`:

```powershell
git switch main
git merge --no-ff lab4-docker
git push origin main
```

## GitHub

Репозиторий опубликован на GitHub: [github.com/edselyoun89/RSP](https://github.com/edselyoun89/RSP). Локальная папка уже подключена к нему как `origin`.

```powershell
git remote -v
git push -u origin main
```

Для следующих лабораторных используйте ветки от актуального `main`, затем отправляйте их через `git push -u origin <branch>`.
