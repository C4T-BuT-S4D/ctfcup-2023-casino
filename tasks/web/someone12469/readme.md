# web | someone12469

## Information

someone12469, характеризующийся своей изощренной хитростью и умением обходить самые совершенные системы безопасности, стал обладателем секретной заметки, содержащей информацию о новейших арбалетах их технических характеристиках. Это привлекло внимание наших спецслужб, и ваша миссия — украсть эту заметку и предотвратить возможные утечки технологий.

someone12469, known for their sophisticated cunning and ability to bypass the most advanced security systems, has acquired a secret note containing information about the latest crossbows and their technical specifications. This has caught the attention of our intelligence agencies, and your mission is to steal this note and prevent potential technology leaks.
http://someone12469-b97c00fbe01c08098632648ca0b668bb.ctfcup-2023.ru

## Deploy

```bash
cd deploy
docker compose up --build -d
```

## Public

## TLDR

Mass assignment to rewrite roles

## Writeup (ru)

В profileController.js происходит изменение профиля пользователя следующим образом
```
      for (const key in req.body) {
        user[key] = req.body[key];
      }
```
Следовательно мы можем поменять любые поля у пользователя в БД (смена которых не приводит к конфликтам)
У пользователя есть поле в схеме:
```
  sharedNotes: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Note' }],
```
Поэтому достаточно взять текущий id заметки со страницы task-site.example/profile/someone12469 (он отображается в ссылке кнопки share)
После чего обновить профиль пользователя со значением sharedNotes равным этому id
## Writeup (en)

In profileController.js the user profile is changed as follows
```
       for (const key in req.body) {
         user[key] = req.body[key];
       }
```
Therefore, we can change any user fields in the database (changing which does not lead to conflicts)
The user has a field in the schema:
```
   sharedNotes: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Note' }],
```
Therefore, it is enough to take the current id of the note from the task-site.example/profile/someone12469 page (it is displayed in the share button link)
Then update the user profile with a sharedNotes value equal to this id

## Flag

`ctfcup{54ee928f6194a378bf2e5757cb276519745b9831}`
