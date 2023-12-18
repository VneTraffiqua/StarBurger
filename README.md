# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Установка и настройка

Скачайте код:
```sh
git clone git@github.com:VneTraffiqua/StarBurger.git
```
Установите Docker и Docker-compose. [Ссылка на инструкцию.](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/)

Создайте файл .env в директории `/backend` рядом с файлом `manage.py` со следующими настройками:
* `SECRET_KEY` - cекретный ключ джанго (пример: `django-insecure-0if40nf4n11111`)
* `YANDEX_TOKEN` - API ключ от яндекс гео-кодера(пример: `3f5d3d66-4180-482f-b2c1-467d7233a111`). Получить его можно в [кабинете разработчика](https://developer.tech.yandex.ru/services/)
* `DEBUG` - hежим отладки (True/False)
* `ROLLBAR_ENVIROMENT` - окружение rollbar, можно указать `production`
* `ROLLBAR_TOKEN` - токен rollbar (пример: `8b98e770028c46b1b63198b206f7a111`)
* `DB_URL` - url адрес базы данных в PostgreSQL. Cформируйте url адрес вашей базы данных по шаблону: `postgres://имя пользователя базы данных:пароль базы данных@db:порт/название базы данных` (пример: `postgres://root:password@db:5432/starburger`)
* `POSTGRES_USER` имя пользователя базы данных
* `DB_PASS` - Пароль от базы данных
* `POSTGRES_DB` - название базы данных
* `POSTGRES_PASSWORD` - пароль базы данных
* `PGDATA` - путь хранения для базы данных (пример: `/var/lib/postgresql/data/pgdata`)

## Dev-версия сайта

Перейдите в директорию проекта и запустите `docker-compose.dev.yml` командой:
```commandline
docker-compose -f docker-compose.dev.yml up -d
```
Сайт будет доступен на локальном хосте.

## Prod-версия сайта

Перейдите в директорию проекта и запустите `docker-compose.prod.yml` командой:
```commandline
docker-compose -f docker-compose.prod.yml up -d
```
Далее, установите сертификат командой:
```commandline
docker-compose -f docker-compose.prod.yml run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d burger-em.ru
```

Перезапустите Nginx:
```commandline
docker-compose restart
```
или
```commandline
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

Обновляйте сертификаты безопасности

Сертификаты Let's Encrypt действительны в течение трех месяцев, после чего необходимо их продлить. Чтобы обновить сертификаты, выполните следующую команду:
```commandline
docker-compose -f docker-compose.prod.yml run --rm certbot renew
```
### Сайт доступен по адресу [burger-em.ru](https://burger-em.ru)

======================================================================