---
title: Ошибки и спорные платежи
description: Что делать, если с переводом что-то не так.
---

## Таблица ситуаций

| Ситуация | Что произойдёт | Что делать вам |
|---|---|---|
| Отправили **не ту сумму** по заявке (TRC20/BEP20) | Платёж станет «неопознанным» | Напишите в поддержку: хэш перевода + номер заявки |
| Оплатили **после 30 минут** | Найдётся и зачислится сам | Ничего |
| Сумма **меньше минимума** | Статус «Меньше минимума», фишки не выдаются автоматически | Напишите в поддержку с номером `DEP-…` |
| Отправили **в другой сети** (например, BEP20 на адрес TRC20) | Перевод не придёт на адрес клуба в нужной сети | Сразу в поддержку с хэшем; вернуть удаётся не всегда |
| Отправили **другую монету** на адрес TON | Не учитывается | В поддержку с хэшем |
| Неверный **ID в ClubGG** | Фишки могут уйти на чужой ID | Сразу в поддержку |
| Снятие **не принимается** в сети | У клуба сейчас не хватает средств в этой сети | Другая сеть или меньшая сумма |

## Как команда разбирает «неопознанные»

```d2 title="Разбор неопознанного платежа"
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
a: "Платёж не совпал\nни с одной заявкой" {class: bad}
b: "Раздел «Неопознанные»\nв админке" {class: team}
c: "Игрок пишет в поддержку:\nхэш перевода, номер заявки" {class: you}
d: Хэш и адрес совпадают? {class: ask}
e: "Пополнение оформляется вручную,\nфишки выдаются" {class: ok}
f: Поддержка уточняет у игрока {class: muted}
g: "Отмечается «Разобрано»" {class: team}
a -> b
b -> c
c -> d
d -> e: да
d -> f: нет
e -> g
```

Все ручные действия команды попадают в [журнал операций](/architecture/audit-log/).
