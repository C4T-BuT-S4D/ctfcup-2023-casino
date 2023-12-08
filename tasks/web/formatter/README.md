# web | Formatter

## Information

Работяги Арбалетов обычно используют древние технологии, не то что мы... Глянь-ка какой мы новомодный форматтер для любых нужд разработали!

The Arbalests seemingly always use some incredibly old technologies, unlike us... Check out the new and modern formatter we've developed! 

[https://formatter-2aa3925d6f934a60479eead292f3943b.ctfcup-2023.ru](https://formatter-2aa3925d6f934a60479eead292f3943b.ctfcup-2023.ru)

## Deploy

```bash
cd deploy
FORMATTER_FLAG="ctfcup{flag}" docker compose up -p web-formatter --build -d
```

## Public

Provide zip archive: [public/formatter.zip](public/formatter.zip).

## TLDR

Path traversal through the "formatter" argument allows executing and writing nearly arbitrary files, which can be used to create and call a custom formatter.

## Writeup (ru)



## Writeup (en)



## Flag

`ctfcup{formatting-is-extremely-dangerous-e7a0ae41b61b10e2}`
