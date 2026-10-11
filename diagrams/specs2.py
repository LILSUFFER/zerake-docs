# Structure diagram (components, not a process). Same notation as specs.py.
from specs import N

SPECS2 = {}

SPECS2["architecture"] = {
    "title": "Как запрос проходит через Zerake",
    "lanes": ["Игрок / команда", "Мини-приложение / админка", "Сервер Zerake", "Внешние системы"],
    "nodes": [
        N("s", "Игрок / команда", 0, "Игрок\nили менеджер", "start"),
        N("ui", "Мини-приложение / админка", 1, "Мини-приложение\nили админка"),
        N("cron", "Сервер Zerake", 0, "Планировщик\nраз в минуту", "start"),
        N("api", "Сервер Zerake", 2, "Серверные функции:\nвсе проверки"),
        N("chain", "Внешние системы", 2, "Блокчейны: поиск\nплатежей и выплаты"),
        N("db", "Сервер Zerake", 3, "База данных\n(правила доступа)"),
        N("log", "Сервер Zerake", 4, "Журнал операций\n(только дописывание)"),
        N("note", "Сервер Zerake", 5, "Уведомления"),
        N("bots", "Внешние системы", 5, "Боты Telegram:\nигроки и команда", "end"),
        N("queue", "Сервер Zerake", 6, "Очередь выдачи\nфишек"),
        N("agent", "Внешние системы", 6, "Агент → ClubGG:\nвыдача фишек", "end"),
    ],
    "edges": [("s", "ui"), ("ui", "api", None, "bottom"), ("cron", "api"), ("api", "chain"), ("api", "db"), ("db", "log"),
              ("log", "note"), ("note", "bots"), ("note", "queue"), ("queue", "agent")],
}
