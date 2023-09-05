# Welcome to my first parser :)
# -*- coding: utf-8 -*-
import copy
import pickle
from datetime import datetime as DT
import os
import re
import urllib.parse
from time import sleep
from user_agent import generate_user_agent
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as My_DriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style

def my_browser_chrome(load_strategy ='normal'):
    # Генерация случайного user-agent
    ua_string = generate_user_agent(os=None, navigator=None, platform=None, device_type="desktop")

    # loads Chrome webdriver 114.0.5735.90
    # servise = Service(executable_path=ChromeDriverManager(driver_version='114.0.5735.90').install())

    os_name = os.name
    if os_name == 'nt':
        servise = Service(executable_path=ChromeDriverManager().install())
    else:
        """Вариант загрузки драйвера для linux"""
        servise = Service(executable_path="/usr/bin/chromedriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = "/usr/bin/chromium-browser"


    # Опции запуска Chrome webdriver
    chrome_options = webdriver.ChromeOptions()

    # chrome_options.page_load_strategy = 'normal'
    chrome_options.page_load_strategy = load_strategy

    # Подмена юзер агента на рандомный
    chrome_options.add_argument(f'--user-agent={ua_string}')

    # Отмена загрузки изображений
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    """блок отвечает за отключение обнаружения автоматизации"""
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--incognito')

    """Дополнительные настройки"""
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--homedir=/tmp")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")
    chrome_options.add_argument('--window-size=1000,500')

    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument('--headless')


    chrome_browser = webdriver.Chrome(options=chrome_options, service=servise)
    print(f'\n{Fore.GREEN}user-agent: {ua_string} {Style.RESET_ALL}\n')

    return chrome_browser

class Parsing:
    URL = 'https://miningpoolstats.stream/#'
    COINS_NEXT = '//li[@id="coins_next"]/a[@aria-controls="coins"]'
    LAST_NUBER_COINS = '(//span[@class="homenr"])[last()]'
    my_list = []

    def __init__(self):
        self.browser = my_browser_chrome()

    def go_too_page(self):
        self.browser.get(self.URL)


    def find(self,
            locator,
            exeptions_text = 'Елемент не найден'):

        """Поиск элемента на странице

        :param locator: (str) локатор
        :param exeptions_text: (str) текст исключения
        """
        try:
            element = My_DriverWait(self.browser, 15, 1).until(EC.visibility_of_element_located(('xpath', locator)))
            return element

        except TimeoutException:
            print(exeptions_text)


    def go_too_element(self, element):
        """Перемещает фокус к элементу

        :param element: (str) принимает локатор
        """
        elem = self.find(element,  'Перемещение к обьекту невозможно, елемент не видно')
        self.browser.execute_script("return arguments[0].scrollIntoView();", elem)


    def pars_text_and_clear(self):
        """Парсит страницу и регуляркой очищает до нужных данных"""
        responce = self.browser.page_source
        text = urllib.parse.unquote(responce).encode('utf-8')
        text = text.decode('utf-8')

        # Очищаем страницу. Берем только тикеры
        clear_text = re.findall(r'homesymbol">(.*?)</small>', text)
        return clear_text


    def swith_too_100(self):
        locator = '//select[@class="form-control input-sm"]'
        locator_100 =  '(//select[@class="form-control input-sm"]/child::*)[3]'
        element = self.find(locator,  'Смена количества монет на странице не отображается')
        element.click()
        sleep(1)

        element_100 = self.find(locator_100,  'Не отображается выбор - 100')
        element_100.click()
        self.go_too_element(locator)
        sleep(1)

    def start_parsing(self):

        last_on_the_list = self.browser.find_element('xpath', self.LAST_NUBER_COINS).text
        # last_on_the_list = int(float(last_on_the_list))
        copy_last_on_the_list = copy.deepcopy(last_on_the_list)

        count = len(self.pars_text_and_clear())
        for i in range(count):
            self.my_list.append(self.pars_text_and_clear()[i])

        obj = self.find(self.COINS_NEXT, 'Кнопка не отобразилась')
        self.go_too_element(self.COINS_NEXT)
        obj.click()
        # sleep(1)
        last_on_the_list = self.browser.find_element('xpath', self.LAST_NUBER_COINS).text

        if copy_last_on_the_list != last_on_the_list:
            self.start_parsing()

        pars_tuple = set(self.my_list)
        return pars_tuple


    def work_start(self):

        def main():
            # Путь к файлу
            file_path = "data.pickle"

            # Дата и время
            data_and_time = str(DT.now())
            old_time = re.sub(r"\.\d+", "", data_and_time)

            # Множество данных который спарсили с сайта
            data = self.start_parsing()
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
#             repo_path = 'https://github.com/sapfire65/stat_parser/'
#             repo = git.Repo(repo_path)
#
#             # Установите переменную окружения GIT_SSH_COMMAND для указания вашего ключа SSH
#             ssh_key_path = 'SSH_KEY'
#             os.environ['GIT_SSH_COMMAND'] = f'ssh -i {ssh_key_path}'
#
#             # Выполняем git push
#             repo.remotes.origin.push()
#
#             print("Git push успешно выполнен с использованием SSH-ключа")
#         except Exception as e:
#             print(f"Произошла ошибка: {e}")




go = Parsing()
go.go_too_page()
go.swith_too_100()

go.start_parsing()
go.work_start()

# go_git = Git()
# go_git.git_push_with_ssh_key()

