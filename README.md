﻿##  Парсер сервиса https://miningpoolstats.stream
По просьбе https://t.me/adobeservice

### Собирает общее количество тикеров на сервисе. 
1) Переключает страницу в режим отображения 100 тикеров
2) Прокликивает все страницы пополняя список тикеров в переменной
3) Записывает данные в файл adta.pickle
4) В зависимости от условий в логике записывает / обновляет данные в файле
5) Скрипт сравнивает старый и новый список и выявляет появление новых тикеров
6) Выводит информацию в консоли о статусе проделанной работы

Реализован GIT-CI запуск в докер образе.

Дополнительно:
- генерация random user-agent для каждой новой сессии
- настройки Chrome Otions для антибот детектера
- адаптация запуска chrome драйвера в зависимости от OS (windows / linux)

p/s Данные  data.pickle не обновляются потому что не пушатся в репозиторий.
База данных актуальна и может быть использована по назначению прям с GIT-CI


Обновление данных: 
### Дата записи файла adta.pickle: 2023-09-05 22:11:47

Projekt import:
copy / pickle / datetime / os / re / urllib.parse / time / user_agent / selenium / 
webdriver_manager / colorama 

tg: https://t.me/Zontiq
Рад общению и сотрудничеству.
