# Обучаемый бот службы техподдержки

Проект предназначен для осуществления техподдержки платформы `Игра Глаголов` в соцсетях Вконтакте и Telegram. Бот отвечает на типичные вопросы пользователей после обучения на платформе [DialogFlow](dialogflow.com).

### Пример работы бота

![Chat example](chat.gif)

### Как установить

1. Python3 должен быть уже установлен.  

2. Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
3. Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.

4. Получить файл с правами `credentials.json` по инструкции [от сюда](https://cloud.google.com/dialogflow/docs/quick/setup). [
    `Create project` -> 
    `Enable the Api` -> 
    `Set up authentication (Create a service account and download the private key file)`
    ]. Полученный файл положить в папку проекта, указать к нему путь в файле `.env` под именем `GOOGLE_APPLICATION_CREDENTIALS`.

5. Создать агента на [DialogFlow](dialogflow.com), установить русский язык общения и привязать к нему созданный проект Google. Project ID из настроек агента положить в `.env` под именем `DIALOGFLOW_PROJECT_ID`.

6. Для работы с Api Вконтакте требуется получить токен группы (вкладка "Работа с API" в настройках сообщества) и разрешить ему отправку сообщений. Полученный токен в `.env` под именем `VK_GROUP_MESSAGE_TOKEN`.

7. Для работы с Telegram потребуется:
    * Включить `VPN`, если мессенджер заблокирован в вашей стране; 
    * Получить `bot token` и положить его в `.env` под именем `TG_BOT_TOKEN`, об этом [здесь](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/);
    * Получить `bot token` для бота-логера, требуемого для отслеживания ошибок в работе ботов. Полученный token в `.env` под именем `TG_LOG_BOT_TOKEN`.

8. Запустить файлы `vk_bot.py` и `tg_bot.py`.

Для обучения бота:

1. Отредактируйте файл `questions.json` по своим требованиям, соблюдая представленное оформление.

2. Запустите функцию `train_bot()` из файла `dialogflow_aps.py`.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
