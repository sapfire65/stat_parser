﻿##  Парсер сервиса https://miningpoolstats.stream
По просьбе https://t.me/adobeservice

### Собирает новые тикеры на сервисе. 
1) Записывает данные в файл adta.pickle
2) В зависимости от условий в логике записывает / обновляет данные в файле
3) Скрипт сравнивает старый и новый список и выявляет появление новых тикеров
4) Выводит информацию в консоли о статусе проделанной работы

Реализован:
- Каждые 30 минут GIT-CI запуск в докер образе.
- Delete workflow runs (удаление всех ранеров кроме пяти крайних)

p/s Данные  data.pickle не обновляются потому что не пушатся в репозиторий.
База данных актуальна и может быть использована по назначению прям с GIT-CI


Обновление данных: 
### Дата записи файла adta.pickle: 2023-09-05 22:11:47

Projekt import:
copy / pickle / datetime / os / re / .parse / time / user_agent / colorama 

tg: https://t.me/Zontiq
Рад общению и сотрудничеству.
