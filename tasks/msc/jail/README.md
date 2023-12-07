# msc | Jail

## Information

Любой уважающий себя житель Metra Veehkim хотя бы раз сидел в тюрьме Арбалетов.

Any self-respecting citizen of Metra Veehkim served time in the Arbalests jail at least once.

[TASK_URL/escape](TASK_URL/escape)

## Deploy

```bash
cd deploy
JAIL_FLAG="ctfcup{flag}" docker compose -p misc-jail up --build -d
```

## Public

Provide zip archive: [public/jail.zip](public/jail.zip).

## TLDR

Escape the jail by deleting global variables and overriding the access whitelist.

## Writeup (ru)

При вызове единственного эндпоинта сервиса, исполняется скрипт, переданный ему в теле запроса, с помощью интерпретатора скриптового языка [Anko](https://github.com/mattn/anko). Судя по конфигурации сервиса, требуется получить доступ ко `/flag`, но нам разрешено чтение с помощью функции `read` только из папок `/jokes` и `/tools`. Так как функция `read` достаёт вайтлист каждый раз из окружения, специально настраимого для исполнения, то, по идее, вайтлист можно переписать, однако, в качестве окружения исполнения передаётся не глобальный контекст, а дважды наследуемый от него, с перетёртым значением `whitelist`. Для решения можно воспользоваться возможностью манипуляции "глобальных" переменных, в частности, удаления, с помощью выражения вида `delete("переменная", true)`, которое найдёт и удалит переменную в глобальном окружении, а не только текущим. Благодаря этому, можно удалить то значение, которое перетирает настоящий вайтлист, и изменить глобальный вайтлист:

```bash
curl $TASK_URL/escape --data-raw 'delete("whitelist", true); whitelist[0] = "/"; read("/flag")'
```

## Writeup (en)

When the only endpoint of the service is called, the script passed in the body of the request is executed by an interpreter of the [Anko](https://github.com/mattn/anko) script language. Judging by the service configuration, access to `/flag` is required, however, reading using the defined `read` function is allowed only from the whitelisted `/jokes` and `/tools` directories. Now, since the `read` function accesses the whitelist by explicitly getting it from the execution environment each time, it should be possible to overwrite the whitelist, however, the execution environment available to us is actually doubly nested in the global environment, with the `whitelist` variable additionally overwritten. To solve the task it is enough to leverage the support for global variable manipulations, specifically, their deletion using expressions of the form `delete("variable", true)`, which will find and delete a variable in the global execution environment, instead of just the current. Using this, the empty whitelist variable can be deleted, and then the actual whitelist can be modified:

```bash
curl $TASK_URL/escape --data-raw 'delete("whitelist", true); whitelist[0] = "/"; read("/flag")'
```

## Flag

`ctfcup{escape-this-wretched-jail-you-have-e5f67a79a95be05094b8d46cf44520f3}`
