---
title: Как сервер находит платёж
description: Проверка блокчейнов, подтверждения и защита от двойного зачисления.
---

## По шагам

1. Планировщик запускает проверку **каждую минуту**.
2. Все четыре сети проверяются **одновременно**: медленная сеть не задерживает остальные.
3. Для каждой сети берутся **новые входящие переводы** на адреса клуба с прошлой проверки.
4. Чтобы ничего не пропустить, окно поиска **перекрывается** с прошлым на 15 минут.
5. Учитываются только **подтверждённые** переводы:
   - **Tron** — подтверждённые сетью;
   - **BNB Chain** — когда над блоком с переводом есть ещё **12 блоков**;
   - **TON** — финализированные транзакции.
6. Каждый перевод сопоставляется:
   - TRC20/BEP20 — с открытой заявкой по **адресу и точной сумме**;
   - TON/GRAM — с игроком по **личному адресу**.
7. Перевод записывается по паре **«сеть + хэш перевода»**. Эта пара уникальна в базе — один перевод **нельзя зачислить дважды**, даже если проверка увидит его снова.
8. Переводы **между адресами клуба** (объединение средств, газ) пополнениями не считаются.

```d2 title="Как сервер разбирает каждый перевод"
classes: {
  zk: {style: {fill: "#e7f8f0"; stroke: "#12a477"; font-color: "#0b3d2c"; border-radius: 10; stroke-width: 2}}
  you: {style: {fill: "#f4f4f5"; stroke: "#a1a1aa"; font-color: "#1d1d1f"; border-radius: 10; stroke-width: 2}}
  chain: {style: {fill: "#eaf1fd"; stroke: "#4c7be0"; font-color: "#1b3a78"; border-radius: 10; stroke-width: 2}}
  team: {style: {fill: "#f3efff"; stroke: "#7c5cd6"; font-color: "#3a2a73"; border-radius: 10; stroke-width: 2}}
  ask: {style: {fill: "#fff8e6"; stroke: "#d6a019"; font-color: "#5c4300"; border-radius: 10; stroke-width: 2}}
  ok: {style: {fill: "#12a477"; stroke: "#0f8a63"; font-color: "#ffffff"; border-radius: 10; stroke-width: 2; bold: true}}
  bad: {style: {fill: "#fdeeee"; stroke: "#d64545"; font-color: "#7a1f1f"; border-radius: 10; stroke-width: 2}}
  muted: {style: {fill: "#fafafa"; stroke: "#d4d4d8"; font-color: "#6b6b72"; border-radius: 10; stroke-dash: 3}}
  box: {style: {fill: "#fbfbfb"; stroke: "#d4d4d8"; border-radius: 14; font-color: "#6b6b72"; stroke-dash: 3}}
}
(** -> **)[*].style: {stroke: "#8a8f96"; stroke-width: 2; font-color: "#3c3c40"; font-size: 14; italic: false}

direction: down
a: "Новый подтверждённый перевод\nна адрес клуба" {class: chain}
b: "Перевод между\nадресами клуба?" {class: ask}
c: "Уже записан\n(сеть + хэш)?" {class: ask}
skip: Пропустить {class: muted}
net: Какая сеть? {class: ask}
e: "Есть заявка с этим адресом\nи точной суммой?" {class: ask}
g: "За кем закреплён адрес?\nСумма ≥ минимума?" {class: ask}
u: "Неопознанный платёж\n→ команда разбирает" {class: bad}
m: "DEP-… «Меньше минимума»" {class: bad}
f: "DEP-… «Получено»" {class: ok}
q: Очередь выдачи фишек {class: zk}
a -> b
b -> skip: да
b -> c: нет
c -> skip: да
c -> net: нет
net -> e: TRC20 / BEP20
net -> g: TON / GRAM
e -> f: да
e -> u: нет
g -> f: да
g -> m: нет
f -> q
```

## Сколько ждать

| Этап | Обычно |
|---|---|
| Подтверждение в сети | TRC20 ~1 мин · BEP20 ~10–40 с · TON ~5–10 с |
| Сервер замечает перевод | до 1 минуты |
| Фишки на ID | от нескольких секунд до нескольких минут |
