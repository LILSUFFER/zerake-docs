---
title: Обзор движения средств
description: Куда идут деньги при пополнении и откуда приходят при снятии — коротко и по пунктам.
---

Этот раздел описывает **весь путь денег**: от вашего кошелька до фишек на ID в ClubGG и обратно. Каждый шаг расписан отдельно, у каждого процесса своя схема (нажмите на схему, чтобы открыть её на весь экран).

## Карта

```d2 title="Карта движения средств"
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
p: "Ваш кошелёк\nили биржа" {class: you}
in: Пополнение {
  class: box
  a1: "Общий адрес клуба\nTRC20 / BEP20" {class: chain}
  a2: "Персональный адрес клуба\nTON / GRAM" {class: chain}
}
s: "Zerake\nнаходит платёж" {class: zk}
g: "Фишки на вашем\nID в ClubGG" {class: ok}
out: Снятие {
  class: box
  w: "Проверка средств\nклуба и выплата" {class: zk}
}
b: "Ваш привязанный\nкошелёк" {class: you}
p -> in.a1: "1 · USDT"
p -> in.a2: "1 · USDT / GRAM"
in.a1 -> s: 2
in.a2 -> s: 2
s -> g: "3 · 1 USDT = 1 фишка"
g -> out.w: "4 · заявка на снятие"
out.w -> b: "5 · USDT / GRAM"
```

## Главное в десяти пунктах

1. **1 фишка = 1 USDT.** GRAM пересчитывается по курсу.
2. Пополнять можно в **четырёх вариантах**: USDT в сетях TRC20, BEP20 и TON, монета GRAM.
3. В **TRC20 и BEP20** пополнение идёт по **заявке**: точная сумма и адрес, 30 минут. [Подробнее](/money/deposit-request/)
4. В **TON и GRAM** за вами закреплён **персональный адрес клуба**: любая сумма, без срока и комментария. [Подробнее](/money/deposit-personal/)
5. Пополнять можно **с любого кошелька**, в том числе с биржи.
6. Сервер проверяет все адреса **раз в минуту** и сам сопоставляет платёж с вами. [Подробнее](/money/detection/)
7. Снятие уходит **только на привязанный кошелёк** этой сети.
8. Перед снятием сервер **проверяет, хватает ли у клуба денег** в этой сети. [Подробнее](/money/withdrawal/)
9. Выплата идёт **напрямую с адресов, куда пришли пополнения**, без промежуточных кошельков. [Подробнее](/money/payout-sources/)
10. Комиссию при снятии берём **только в TRC20** (3 USDT + 1%). [Подробнее](/money/fees/)

## Сети одной таблицей

| | TRC20 | BEP20 | TON (USDT) | GRAM |
|---|---|---|---|---|
| Блокчейн | Tron | BNB Chain | TON | TON |
| Способ пополнения | заявка на общий адрес | заявка на общий адрес | персональный адрес | персональный адрес |
| Мин. пополнение | 10 USDT | 10 USDT | 1 USDT | $1 в GRAM |
| Мин. снятие | 10 | 10 | 10 | 5 |
| Комиссия снятия | 3 USDT + 1% | 0 | 0 | 0 |
| Когда платёж считается подтверждённым | подтверждён сетью Tron | 12 блоков | финализирован в TON | финализирован в TON |
