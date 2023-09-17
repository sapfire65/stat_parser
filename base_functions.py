import re


class BaseFunctions:

    @staticmethod
    def reqular_findall(self, text,  before_text, after_text):
        """Регулярное выражение, возвращает список элементов между двумя отрезками строк

            :param text: (str), исходный текст
            :param before_text: (str), фрагмент строки "до" искомого элемента
            :param after_text: (str), фрагмент строки "после" искомого элемента
            """

        return re.findall(fr'{before_text}(.*?){after_text}', text)




