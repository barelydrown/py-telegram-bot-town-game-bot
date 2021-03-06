# **[Города](https://t.me/town_game_bot) — телеграм-бот**
### [`@town_game_bot`](https://t.me/town_game_bot) — бот, который умеет играть с пользователем в города.
Города — игра для нескольких (двух или более) человек, в которой каждый участник в свою очередь называет реально существующий город любой страны, название которого начинается на ту букву, которой оканчивается название предыдущего города. 

_Например:  
Игрок №1: Росто**в**  
Игрок №2: **В**ыбор**г**  
Игрок №1: **Г**еленджи**к**  
Игрок №2: **К**азань_  

Повторения не допускаются. Игра оканчивается, когда участник не может назвать нового города.
___

#### `Бот имеет два режима игры:`
* **Города** 🇷🇺 **(РФ)**
* **Города** 🌎 **(Мир)**

В режиме **Города** 🇷🇺 в базе бота находятся все города, входящие в состав Российской Федерации (около 1100).   
_Примечание: В РФ населённый пункт может приобрести статус города, если в нём проживает не менее 12 тысяч жителей._

В режиме **Города** 🌎 в базе бота числится более 10 000 городов всех стран мира.
___
#### `Логика работы:` 
Данный Бот проверяет каждую букву города с конца и отправляет вспомогательное сообщение, в случае, если следующий город должен начинаться не с последней буквы предыдущего. Вспомогательное сообщение содержит букву, на которую должен начинаться следующий город, а также буквы(у), которые не могут быть использованы.

Буквы могут не пройти проверку: 
- если на них не начинается ни один город (например: Ь, Ъ); 
- если городов на данную букву не осталось (они были уже названы ранее) 

***Каждый город, отправленный ботом также является ссылкой, нажав на которую можно более подробно ознакомится с населенным пунктом в интернете.***
___
#### `Telegram:`
Сам бот: [@town_game_bot](https://t.me/town_game_bot)  
Автор бота: [@drownpierrot](https://t.me/drownpierrot)
