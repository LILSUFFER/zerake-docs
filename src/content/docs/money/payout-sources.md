---
title: Откуда идёт выплата
description: Как сервер выбирает адреса и почему вы всегда получаете один перевод.
---

## Правило выбора

1. Сервер смотрит баланс **каждого адреса клуба** в нужной сети.
2. У каждого адреса оставляется запас на его собственную комиссию.
3. Если есть **один адрес, где хватает на всю выплату**, — платит с **самого маленького** из таких (крупные остаются для крупных выплат).
4. Если **ни на одном** не хватает — собирает сумму с нескольких адресов, **начиная с самых крупных**.

```d2 title="Как выбирается адрес для выплаты"
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
a: Нужно выплатить X {class: you}
b: "Есть адрес,\nгде лежит ≥ X?" {class: ask}
c: "Взять самый маленький\nиз подходящих" {class: zk}
d: "Набрать X с нескольких адресов,\nначиная с крупных" {class: zk}
e: Сеть TON или GRAM? {class: ask}
f: "Перевести части на один адрес\n(+ запас на газ) и дождаться" {class: zk}
h: "Переводы частями\nс каждого адреса" {class: zk}
pay: Один перевод игроку {class: ok}
a -> b
b -> c: да
b -> d: нет
c -> pay
d -> e
e -> f: да
e -> h: "нет: TRC20 / BEP20"
f -> pay
```

## Газ (комиссия сети) при выплате

| Сеть | Кто платит газ | Как |
|---|---|---|
| **TRC20** | игрок (в комиссии снятия) | Сервис GasFree списывает плату в USDT прямо с адреса пула — TRX не нужен |
| **BEP20** | клуб | Адрес для комиссий докидывает BNB на платящий адрес перед переводом |
| **TON (USDT)** | клуб | Кошелёк клуба докидывает ~0.07 GRAM на платящий адрес |
| **GRAM** | клуб | Газ берётся из запаса на самом адресе |

## Почему в TON и GRAM один перевод

Игроку удобнее получить **одну** транзакцию. Поэтому в TON и GRAM части сначала объединяются на одном адресе клуба, и только потом уходит один перевод вам. Каждая часть идёт **с небольшим запасом на газ** — приём перевода тоже стоит немного газа, и без запаса на адресе могло бы не хватить нескольких тысячных.

Если объединение не завершилось, **игроку ничего не отправляется** — деньги остаются у клуба, заявка возвращается команде.
