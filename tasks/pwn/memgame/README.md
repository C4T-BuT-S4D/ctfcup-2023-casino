# pwn | Memgame

## Information

> Искуственный интеллект Megalith хорош не только в обеспечении стабильности и эффективности управления планетой, но и в играх.
>
> Megalith AI is great not only in providing the stability and efficiency of running a planet, but in games, too.
> 
> `nc memgame-28bedf331f28000df86f38b87c842ed9.ctfcup-2023.ru 13003`

## Deploy

```sh
cd deploy/
docker compose up --build -d
```

## Public

Provide zip file [public/memgame.zip](./public/memgame.zip)

## TLDR

Ликнуть адрес либсы и бинаря, переписать `DT_STRTAB` в `link_map` так, чтобы вместо `rand` вызвался `gets`, записать роп на стек.

## Writeup (ru)

Мы указывает индекс, и если по этому индексу находится число, меньше 0x4000, можем перезаписать следующее за ним число. Ликнем адрес бинаря и адрес link_map через got. 

Дальше в link_map переписываем указатель на `DT_STRTAB` так, чтобы он указывал на контролируемую нами память, туда запишем (адрес строки `gets` из либсы - оффсет строки `rand` в изначальном `STRTAB`). Теперь вместо rand вызовется `gets`, при этом в `rdi` будет лежать адрес стека, который находится выше текущего адреса возврата. Затем аккуратно перепишем адрес возврата из `gets`, не испортив нужные для `gets` указатели, лежащие на стеке.

[Exploit](./solve/sploit.py)

## Flag

```
ctfcup{cb3ab1923902186c22265e33a14e3458}
```

## Cloudflare

No
