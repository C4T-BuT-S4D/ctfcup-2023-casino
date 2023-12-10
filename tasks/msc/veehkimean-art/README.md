# msc | Veehkimean Art

## Information

Известнейший художник с планеты Metra Veehkim нуждается в ассистенте.  
Покажите, что вы идеальный кандидат! `nc art-3b03c4fb9e8f920448ce5b3d18b95d35.ctfcup-2023.ru 12345`.

Famous Metra Veehkimean painter looking to hire an assistant.  
Prove your skills and get the job! `nc art-3b03c4fb9e8f920448ce5b3d18b95d35.ctfcup-2023.ru 12345`

## Deploy

## Public
Provide [zip archive](public/ppc-art.zip).

## TL;DR
Do what needs to be done. Or play it smart (see below).

## Writeup (ru)
[Авторское решение](https://github.com/C4T-BuT-S4D/ctfcup-2023-casino/blob/master/tasks/msc/veehkimean-art/solve/exploit.py) использует адаптированный код библиотеки, которая используется в самом `task.py`.

Заглянем в [исходники](https://github.com/pglass/cube/blob/main/rubik/solve.py) решателя, поставляемого с библиотекой.
Видим, что реализован простейший алгоритм послойной сборки куба. Есть методы, которые реализуют сборку креста и уголков.
Эти методы можно аккуратно скопировать к себе, и, прочитав реализацию, понять, как заставить их перемещать уголки и ребра нужного цвета.

Перед этим нужно правильно ориентировать куб. Этот шаг можно захардкодить.

Решать эту задачу с нуля в рамках формата казино, конечно, не оптимально. Именно поэтому верный подход - попытаться адаптировать
уже существующее решение.

Теперь о непредусмотренном решении.

Я немного увлёкся с рандомизацией в таске. Рандомизировались и выдаваемые кубы, и фон картинки, и порядок, в котором участки 3 на 3 выдавались в раундах. 
При этом текст был всегда написан белым цветом, а на фоне белый цвет не использовался (это было сделано осознанно).

Нетрудно теперь понять, что задачу решать вообще не нужно :) Достаточно очень много раз подключиться к таску, чтобы собрать выдаваемые в первом раунде грани. Таким образом можно собрать картинку целиком. 

![Флаг](solve/flag.png)

## Writeup (en)
The [intended solution](https://github.com/C4T-BuT-S4D/ctfcup-2023-casino/blob/master/tasks/msc/veehkimean-art/solve/exploit.py) adapts the solver which is already present in the library's code.

Let's take a look at the [sources](https://github.com/pglass/cube/blob/main/rubik/solve.py). We see that a simple layer-by-layer approach is used there.
We can also notice there are methods to assemble the cross and corners. We can carefully copy them over to our exploit and realize how to call them
to place arbitrary colored pieces.

Before assembling the face, the cube must be oriented correctly. That part can be hard-coded.

Of course, writing a solution from scratch isn't time effective in a casino format. So the right approach was to read the sources and try to adapt 
them for our problem.

However, there was an unintended solution.

I'll admit, I went overboard with randomization. Pretty much eveything was randomized, including the coordinates of the faces in each round. One thing which wasn't is that the flag was spelled out in white, and the background did not use white. 

This meant that just connecting to the task, without trying to solve the cubes, after many repetitions, would give us enough samples to assemble the flag picture.


![Flag](solve/flag.png)

## Flag
`ctfcup{Cubing_is_art_and_the_stuff_I_cube_is_the_bomb}`
