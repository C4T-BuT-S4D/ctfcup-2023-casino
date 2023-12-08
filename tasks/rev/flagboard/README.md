# rev | FlagBoard
## Information

Пробираясь по коридорам небоскрёба Арбалетов Сибири, вы пришли к укреплённой стальной двери.  
Рядом с дверью - сенсорный экран. Очевидно, на нём нужно набрать секретный код.  
Но почему он подсказывает, какую кнопку нужно нажать дальше?!

Making you way through the corridors of Arbalest of Siberia's skyscraper, you find yourself before a reinforced steel door.  
Next to said door is a touchscreen. Apparently, a secret code needs to be typed on it.  
But why on Earth is the touchscreen telling you what to click next?!

## Deploy

## Public
Provide [public/rev-flagboard.zip](zip archive).

## TL;DR
The app's code was minified, so brute force reversing is suboptimal. To find exactly where we need to look, search for usages of `R.raw.lookforme`, which is a text file in `res/raw` containing info about the levels.

## Flag
`ctfcup{Gu4axf_Sbe-Cynl1at}`
