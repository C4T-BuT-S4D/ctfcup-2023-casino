# rev | C4Tpixx
## Information

Мы тут не всё успели доделать... (Сами понимаете, айти бюджеты на Metra Veehkim невелики.) Но зацените то, что есть! Надеемся, у вас получится разглядеть что-то любопытное.

We couldn't quite finish this one on time... (You know, IT budgets on Metra Veehkim are kind of thin.) Still, look at what we've already got! You might even see some peculiar things if you squint a little.

## Deploy

## Public
Give [zip archive](public/rev-catpixx.zip).

## TL;DR
The app's code was minified, so we'll have to look for clues. One such clue is `android.widget.Toast` shown when we're wrong. We find one suspicious usage in `XXX()`. The method names of xrefs to `XXX()` spell out the flag. This can be seen in logcat, because if we enter the correct secret string, the app crashes with UnsupportedOperationException.

## Writeup (ru)
[Посмотрим на приложение](https://youtu.be/uP0wZM0eHy4). Мы нашли скрытое окно, куда нужно что-то ввести.

Байткод приложения был минифицирован, это можно понять по названиям классов, их полей, методов. Ревёрсить всё это в рамках формата казино, 
конечно же, не предлагалось. Достаточно было зацепиться за строку `Wrong! gas leak`, которая показывается при неудаче. 
Её мы находим в классе `androidx.compose.ui.platform.f1`:
```
$ rg "Wrong! gas leak"
smali/androidx/compose/ui/platform/f1.smali
76:    const-string v1, "Wrong! gas leak"
```

Посмотрим на хрефы к методу `g()`. Видим несколько очень похожих друг на друга методов:
```java
    public static void t(String str) {
        if ((168 ^ str.codePointAt(4)) != 218) {
            androidx.compose.ui.platform.f1.g();
        } else {
            p.u.p(str);
        }
    }
```

Здесь справедливо предположение, что `str` - строка, введенная в текстовое поле, а сами методы проверяют введенную строку, вызывая друг друга
по цепочке. Пощелкаем по вызовам вглубь, *делая это вдумчиво, а может быть, и бубня себе под ноc*. 

Приходим сюда:
```java
package androidx.emoji2.text;

public abstract class f {
    ...
    public static void d(String str) {
        throw new UnsupportedOperationException("Easter egg not implemented yet, sorry");
    }
}
```

В окошко мы должны ввести `5uper_Dup3r Secret String!1`. Но это совершенно очевидно не является флагом. При этом на данном этапе все равно можно
утверждать, что флаг мы видели XD

Возьмём подсказку из названия таска и заглянем в logcat, где будет стакртрейс исключения.
```
VM exiting with result code 0, cleanup skipped.
FATAL EXCEPTION: main
Process: ru.ctfcup.c4tpixx, PID: 5809
java.lang.UnsupportedOperationException: Easter egg not implemented yet, sorry
	at androidx.emoji2.text.f.d(Unknown Source:4)
	at j.d.x7d(Unknown Source:21)
	at a5.j0.h(Unknown Source:21)
	at j4.j.x34(Unknown Source:21)
	at y.u1.o(Unknown Source:21)
	at m.c2.w(Unknown Source:21)
	at j4.m0.x(Unknown Source:21)
	at w0.c.x(Unknown Source:21)
	at n.j.i(Unknown Source:21)
	at p.u.p(Unknown Source:21)
	at d1.j0.t(Unknown Source:21)
	at y0.i.x34(Unknown Source:21)
	at g4.c0.c(Unknown Source:21)
	at x4.n.e(Unknown Source:21)
	at d1.s.c(Unknown Source:21)
	at v4.q.i(Unknown Source:21)
	at y0.b.n(Unknown Source:21)
	at u.u0.h(Unknown Source:21)
	at v2.h.c(Unknown Source:21)
	at j4.p.u(Unknown Source:21)
	at o4.n.s(Unknown Source:21)
	at x4.e.x7b(Unknown Source:21)
	at a0.g2.p(Unknown Source:21)
	at m.g0.u(Unknown Source:21)
	at q2.b.c(Unknown Source:21)
	at k.c0.f(Unknown Source:21)
	at y.s.t(Unknown Source:21)
	at m0.e.c(Unknown Source:21)
	at androidx.compose.ui.platform.j2.b(Unknown Source:13)
	at l.o1.a(Unknown Source:18)
	at l.o1.X(Unknown Source:14)
  ...
	at u.d2.d(Unknown Source:26)
	at x.y.c(Unknown Source:189)
	at androidx.compose.ui.platform.AndroidComposeView.G(Unknown Source:78)
	at androidx.compose.ui.platform.AndroidComposeView.m(Unknown Source:223)
```

Здесь назревает пару вопросов:
1. Почему так глубоко в call stack, где нет даже нормальных имён пакетов, вдруг появляется `androidx.compose.ui...`?
2. Почему в, казалось бы, минифицированном коде, методы называются `x34`, `x7b`, `x7d`?

Ответ простой: методы, конечно же, были впатчены в уже собранное приложение. Но 0x34 - <kbd>4</kbd>, 0x7b - <kbd>{</kbd>, 0x7d - <kbd>}</kbd>. Флаг? Да, флаг. 
Читаем снизу вверх, начиная от "невозможного" `androidx...j2.b()`: `c()` `t()` `f()` `c()`...

## Writeup (en)

Let's [take a look](https://youtu.be/uP0wZM0eHy4) at the app. We find a hidden dialog with a textfield.

The app's bytecode was minified, which is evident from the names of classes, methods and fields. Of course, reversing without some insight is
time-consuming. But we can narrow our search scope.
```
$ rg "Wrong! gas leak"
smali/androidx/compose/ui/platform/f1.smali
76:    const-string v1, "Wrong! gas leak"
```

Taking a look at `f1.g()` it is indeed the "fail" method of the check. Xrefs to `g()` must then implement the check itself.
But the referencing methods are quite similar to each other. They all look like this:
```java
    public static void t(String str) {
        if ((168 ^ str.codePointAt(4)) != 218) {
            androidx.compose.ui.platform.f1.g();
        } else {
            p.u.p(str);
        }
    }
```

We can assume that `str` is the string we entered into the text field. At this point, we can just *mindfully* click through all calls until we arrive here:
```java
package androidx.emoji2.text;

public abstract class f {
    ...
    public static void d(String str) {
        throw new UnsupportedOperationException("Easter egg not implemented yet, sorry");
    }
}
```

The string that we're supposed to enter is `5uper_Dup3r Secret String!1`. Hmm, that's not the flag. 

Taking a hint from the task's name, let's look at the traceback in logcat:
```
VM exiting with result code 0, cleanup skipped.
FATAL EXCEPTION: main
Process: ru.ctfcup.c4tpixx, PID: 5809
java.lang.UnsupportedOperationException: Easter egg not implemented yet, sorry
	at androidx.emoji2.text.f.d(Unknown Source:4)
	at j.d.x7d(Unknown Source:21)
	at a5.j0.h(Unknown Source:21)
	at j4.j.x34(Unknown Source:21)
	at y.u1.o(Unknown Source:21)
	at m.c2.w(Unknown Source:21)
	at j4.m0.x(Unknown Source:21)
	at w0.c.x(Unknown Source:21)
	at n.j.i(Unknown Source:21)
	at p.u.p(Unknown Source:21)
	at d1.j0.t(Unknown Source:21)
	at y0.i.x34(Unknown Source:21)
	at g4.c0.c(Unknown Source:21)
	at x4.n.e(Unknown Source:21)
	at d1.s.c(Unknown Source:21)
	at v4.q.i(Unknown Source:21)
	at y0.b.n(Unknown Source:21)
	at u.u0.h(Unknown Source:21)
	at v2.h.c(Unknown Source:21)
	at j4.p.u(Unknown Source:21)
	at o4.n.s(Unknown Source:21)
	at x4.e.x7b(Unknown Source:21)
	at a0.g2.p(Unknown Source:21)
	at m.g0.u(Unknown Source:21)
	at q2.b.c(Unknown Source:21)
	at k.c0.f(Unknown Source:21)
	at y.s.t(Unknown Source:21)
	at m0.e.c(Unknown Source:21)
	at androidx.compose.ui.platform.j2.b(Unknown Source:13)
	at l.o1.a(Unknown Source:18)
	at l.o1.X(Unknown Source:14)
  ...
	at u.d2.d(Unknown Source:26)
	at x.y.c(Unknown Source:189)
	at androidx.compose.ui.platform.AndroidComposeView.G(Unknown Source:78)
	at androidx.compose.ui.platform.AndroidComposeView.m(Unknown Source:223)
```

One can be asking these questions:
1. What's `androidx.compose.ui.platform.j2.b()` doing so deep into a minified call stack?
2. Why, in a minified bytecode, there are methods named `x34`, `x7b`, `x7d`?

The answer to both is simple: the check was patched into the bytecode. Wait, but 0x34 = <kbd>4</kbd>, 0x7b = <kbd>{</kbd>, 0x7d = <kbd>}</kbd>. 
Are we seeing things? Is that the flag? Let's read from bottom to top, starting with our weird `androidx...j2.b()`: `c()`, `t()`, `f()`, `c()`...

## Flag
`ctfcup{suchnicec4tpixxwo4h}`

<!-- постскриптум: prӧӧӧh about it -->
