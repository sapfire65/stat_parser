# Welcome to my first parser :)
# -*- coding: utf-8 -*-
import copy
import pickle  #  Преобразование /восстановления - объектов Python в байтовые потоки
import os
from colorama import Fore, Style
from base_functions import BaseFunctions


class Parsing:
    URL = 'https://miningpoolstats.stream/newcoins'
    DATA = 'https://data.miningpoolstats.stream/data/coins_data_new.js?t='

    def pars_js_file(self):
        reqular = BaseFunctions.reqular_findall
        request = BaseFunctions.request_and_fake_useragent
        my_resp = request(self.URL)
        clear_text = reqular(my_resp, 'last_time = "', '";var')
        last_time = clear_text[0]
        resoult_url = self.DATA + last_time
        responce = request(resoult_url)
        clear_text = reqular(responce, 'name":"', '","algo')
        clear_text = set(clear_text)
        return clear_text

    def work_start(self):
        data_and_time = BaseFunctions.data_and_time

        def main():
            # Путь к файлу
            file_path = "data.pickle"
            # Дата и время
            old_time = data_and_time()

            # Множество данных который спарсили с сайта
            data = self.pars_js_file()
            # data = {'Новый СУПЕР БИТКОИН'}

            new_data = [old_time, data]
            # print('>>>', new_data)

            # Логика. Проверяем наличие файла с данными data.pickle
            if 'data.pickle'not in os.listdir():
                write_data_to_file(file_path, new_data)  # Записывает данные в файл
                print(f'{Fore.CYAN} \nПервый запуск скрипта! {Style.RESET_ALL}'
                      '\n Файл данных - создан.'
                      '\n Данные сайта miningpoolstats сохранены.'
                      '\n Сравнительный анализ после повторного запуска скрипта. ')

            else:
                print(f'{Fore.BLUE}\nСтатус сравнения:{Style.RESET_ALL}')
                old_count = open_and_read_file(file_path)  # Читает данные с файла

                new_count = copy.deepcopy(data) # список тикеров типа set

                status = new_count - old_count[1]  #  новые данные - старые из файла
                list_status = list(copy.deepcopy(status))
                count_elements_in_list = len(list_status)
                if count_elements_in_list == 0:
                    print(f'{Fore.YELLOW}На miningpoolstats без изменений.{Style.RESET_ALL}')
                else:
                    print(f'{Fore.GREEN}ВНИМАНИЕ НОВЫЕ ТИКЕРЫ!{Style.RESET_ALL}')
                    for i in range(count_elements_in_list):
                        print(f'{list_status[i]} \n')
                    #  Перезапись новой информации в файл
                    write_data_to_file(file_path, new_data)
                    print(f'>>{Fore.YELLOW}Update complete{Style.RESET_ALL}')


        def write_data_to_file(file_path, data):
            """Запись данных в файл"""
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            write = open_and_read_file(file_path)
            print(f'{Fore.RED}Обновление данных: {Style.RESET_ALL}')
            print(f'Дата записи файла: {write[0]}')
            print(f'Теперь в базе: {len(write[1])} тикер(ов) криптовалют')


        def open_and_read_file(file_path):
            """Читает данные с файла"""
            with open(file_path, 'rb') as f:
                data_new = pickle.load(f)
                return data_new

        main()



# class Git:
#     def git_push_with_ssh_key(self):
#         try:
#             # Укажите путь к вашему репозиторию
#             repo_path = 'sapfire65/stat_parser/'
#             repo = git.Repo(repo_path)
#
#             # Установите переменную окружения GIT_SSH_COMMAND для указания вашего ключа SSH
#             ssh_key_path = secrets.CI_TOKEN
#             os.environ['GIT_SSH_COMMAND'] = f'ssh -i {ssh_key_path}'
#
#             # Выполняем git push
#             repo.remotes.origin.push()
#
#             print("Git push успешно выполнен с использованием SSH-ключа")
#         except Exception as e:
#             print(f"Произошла ошибка: {e}")


go = Parsing()
ip = BaseFunctions()

go.pars_js_file()
go.work_start()
ip.check_ip()


