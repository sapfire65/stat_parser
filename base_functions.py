import re
import requests
from user_agent import generate_user_agent
from datetime import datetime as DT


class BaseFunctions:

    @staticmethod
    def reqular_findall(text,  before_text, after_text):
        """Регулярное выражение, возвращает список элементов между двумя отрезками строк

            :param text: (str), исходный текст
            :param before_text: (str), фрагмент строки "до" искомого элемента
            :param after_text: (str), фрагмент строки "после" искомого элемента
            """

        return re.findall(fr'{before_text}(.*?){after_text}', text)

    @staticmethod
    def request_and_fake_useragent(url):
        """Запрос + генерированный User-Agent
        :param url: (str), адрес запроса
        """
        # Генерация случайного user-agent
        fake_user_agent = {'User-Agent': generate_user_agent(os=None, navigator=None, platform=None, device_type="desktop")}
        return requests.get(url, headers=fake_user_agent).text


    @staticmethod
    def data_and_time():
        # Дата и время
        data_and_time = str(DT.now())
        return re.sub(r"\.\d+", "", data_and_time)



