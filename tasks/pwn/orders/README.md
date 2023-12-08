# pwn | Orders

## Information

> Только сегодня и только сейчас! Качественные арбалеты с большой скидкой! Ищите в ближайшем магазине Арбалетов Сибири своего города!
> 
> Only today and only now! Quality arbalests with a huge discount! Find 'em in the closests Arbalety Sibiri shop of your city!
> 
> `nc orders-05f347c5e71ab904171cd11f1cb2b9f6.ctfcup-2023.ru 13002`

## Deploy

```sh
cd deploy/
./build.sh
```

## Public

Provide zip file [public/orders.zip](./public/orders.zip)

## TLDR

Ликнуть адрес либсы из .got, ликнуть адрес стека из переменной `environ` в либсе, переписать `strlen` на `system`

## Writeup (ru)

Когда мы вводим индекс массива, он никак не проверяется, поэтому можно передать отрицательный индекс и прочитать адрес из .got таблицы.

Также, при редактировании заказа мы можем писать в `/proc/self/mem`. Для получения шелла перепишем адрес `strlen` из .got бинаря на адрес `system`. Для этого нам надо, чтобы где-то в бинаре появился адрес system. Тогда мы сможем посчитать правильный оффсет от этого адреса до массива и сделать перезапись.

Запишем адрес `system` на стек во время чтения имени файла в `edit`, то есть запишем его сразу после имени файла: `'../../../proc/self/mem\0\0'+p64(libc.sym.system)`. После того, как мы переписали `strlen` на `system`, передадим `/bin/sh\0` в качестве `order_id` в функции `get`.

[Exploit](./solve/sploit.py)

## Flag

```
ctfcup{17fa166ba31d4a433d26269cbfe5ec25}
```

## Cloudflare

No
