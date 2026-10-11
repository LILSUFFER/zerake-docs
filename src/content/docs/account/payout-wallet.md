---
title: Кошелёк для выплат
description: Почему выплаты уходят только на один привязанный кошелёк и как его выбрать.
---

В каждой сети вы привязываете **один личный кошелёк**. Снятие фишек в этой сети приходит **только на него**.

| Сеть | Какой адрес нужен |
|---|---|
| TRC20 | Адрес Tron, начинается с `T` |
| BEP20 | Адрес BNB Chain, начинается с `0x` |
| TON и GRAM | Один адрес TON (`UQ…` или `EQ…`) на обе |

## Зачем это нужно

Даже если кто-то получит доступ к вашему Telegram, он **не сможет вывести деньги на свой кошелёк**: выплаты идут только на привязанный адрес, а сменить его можно лишь [секретной фразой и через 48 часов](/account/recovery/).

```d2 title="Выплата только на привязанный кошелёк"
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
a: Запрос на снятие {class: you}
b: "Кошелёк в этой сети\nпривязан?" {class: ask}
x: "Снять нельзя:\nсначала привяжите кошелёк" {class: bad}
c: "Выплата только\nна привязанный адрес" {class: zk}
d: Ваш кошелёк {class: ok}
a -> b
b -> x: нет
b -> c: да
c -> d
```

## Как привязать

1. Вкладка **Купить** → выберите сеть.
2. Вставьте адрес **своего личного** кошелька (Trust Wallet, Tonkeeper, MetaMask и т. п.).
3. Отметьте «Это мой личный кошелёк, а не адрес биржи» → **Привязать кошелёк** → подтвердите.

Привязка нужна до первого пополнения в этой сети.

## Пополнять можно с любого кошелька

Кошелёк для выплат и кошелёк, **с которого** вы пополняете, — разные вещи. Пополнять можно откуда угодно: с биржи, из @wallet, с чужого кошелька. Выплаты при этом всё равно пойдут только на привязанный.

:::danger[Не привязывайте адрес биржи]
У бирж адрес пополнения может смениться или требовать мемо/комментарий. Выплата может потеряться. Привязывайте адрес кошелька, ключи от которого есть только у вас.
:::

## Один кошелёк — один игрок

Кошелёк, привязанный к одному аккаунту Zerake, нельзя привязать к другому.
