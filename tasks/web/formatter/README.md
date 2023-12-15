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

Сервис, по сути, содержит лишь 2 эндпоинта, связанных с логикой:

1. `/format` - принимает файл, который требуется отформатировать, и название утилиты, которой необходимо отформатировать. Утилита запускается из директории `formatters`, после чего её вывод сохраняется с частично случайным названием в директорию `uploads`.
2. `/uploads/<path:path>` - позволяет прочитать отформатированный файл, если используется известное название.

По коду хэндлера эндпоинта `/format` видно, что аргумент `formatter`, который задаёт название утилиты для форматирования, никак не проверяется и не проходит никакую санитизацию, из-за чего можно проэксплуатировать уязвимость path traversal для запуска собственной утилиты. К тому же, странным образом обрезается итоговое название файла - берутся первые 100 символов уже после того, как составлен полный путь.

Авторское решение предполагает использование утилиты для форматирования `yaml`, которая просто выводит содержимое, для создания собственного скрипта в директории `formatters` за счёт того, что путь, по которому сохраняется отформатированный файл, обрезается. Для этого требуется указать аргумент `formatter` со значением такого вида:

```python
f"../../../formatters/{os.urandom(20).hex()}/../../app/formatters/yaml"
```

Проблема далее заключается в том, что созданный скрипт не будет исполняемым, из-за чего воспользоваться им не получится. Можно заметить, что при запуске приложения происходит добавление всем файлам-форматтерам исполняемого бита:

```python
for formatter in os.listdir("formatters"):
    path = f"formatters/{formatter}"
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
```

Соответственно, требуется всего лишь каким-то образом перезапустить один из воркеров gunicorn. Так как у каждого воркера выставляется таймаут на ответ на конкретный запрос, по умолчанию 30 секунд, можно через path traversal запустить, к примеру, `/usr/bin/yes`, который бесконечно будет выводить `y`, и тем самым заставить gunicorn перезапустить этот воркер.

Это решение представлено в [solve/solve.py](./solve/solve.py). Однако, у задания было и альтернативное решение - можно было сразу воспользоваться `/usr/bin/env`, который просто выводит переменные окружения, где, собственно, и находился флаг.

## Writeup (en)

The service essentially contains only 2 endpoints related to logic:

1. `/format` - accepts a file that needs to be formatted, and the name of the utility to format it with. The utility is run from the `formatters` directory, after which its output is saved with a partially random name in the `uploads` directory.
2. `/uploads/<path:path>` - allows reading the formatted file if a known name is used.

From the code of the `/format` endpoint handler, it is evident that the `formatter` argument, which sets the name of the utility for formatting, is not checked or sanitized in any way, allowing for the exploitation of a path traversal vulnerability to execute one's own utility. Moreover, the final file name is strangely truncated - the first 100 characters are taken after the full path has been composed.

The author's solution involves using a `yaml` formatting utility, which simply outputs the content, to create one's own script in the `formatters` directory by exploiting the fact that the path where the formatted file is saved gets truncated. To do this, you need to specify the `formatter` argument with a value like this:

```python
f"../../../formatters/{os.urandom(20).hex()}/../../app/formatters/yaml"
```

The problem then is that the created script will not be executable, which means it cannot be used. It can be noted that when the application starts, the executable bit is added to all formatter files:

```python
for formatter in os.listdir("formatters"):
    path = f"formatters/{formatter}"
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
```

Accordingly, all that is needed is somehow to restart one of the gunicorn workers. Since each worker has a timeout for a response to a specific request, by default 30 seconds, you can use path traversal to run, for example, `/usr/bin/yes`, which will indefinitely output `y`, thereby forcing gunicorn to restart that worker.

This solution is presented in [solve/solve.py](./solve/solve.py). However, the challenge also had an alternative solution - one could immediately use `/usr/bin/env`, which simply outputs the environment variables, where the flag was actually located.

## Flag

`ctfcup{formatting-is-extremely-dangerous-e7a0ae41b61b10e2}`
