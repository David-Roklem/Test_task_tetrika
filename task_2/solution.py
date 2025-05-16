import mwclient
import csv
from collections import defaultdict


def extract_animals() -> dict:
    """Извлекает данные из википедии, возвращает словарь, где ключ содержит первую букву, с которой начинается
    название животного, а словарь - количество найденных записей об этих животных."""
    site = mwclient.Site("ru.wikipedia.org")

    animals_count = defaultdict(int)
    category = site.categories["Животные по алфавиту"]
    for page in category:
        title = page.name
        if title:
            first_letter = title[0].upper()  # Получаем первую букву
            if "А" <= first_letter <= "Я" or first_letter == "Ё":  # Отфильтровываем все кроме букв русского алфавита
                animals_count[first_letter] += 1  # Увеличиваем счетчик для этой буквы'

    return dict(animals_count)


def custom_sort(letter):
    """Сортирует буквы алфавита так, чтобы 'Ё' шла после буквы 'Е'"""
    if letter == "Ё":
        return "Е", 1  # Возвращаем "Е" и флаг, чтобы "Ё" шла после "Е" при дальнейшей сортировке по ключу
    return letter, 0


def to_file(animals_count: dict):
    """Записывает данные о животных в csv файл."""
    with open("beasts.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for letter in sorted(animals_count.keys(), key=custom_sort):
            writer.writerow([letter, animals_count[letter]])

    print("Данные успешно записаны в файл beasts.csv")


def main():
    animals_count = extract_animals()
    to_file(animals_count)


# if __name__ == "__main__":
#     main()


def test_custom_sort():
    """Тестовые случаи для функции custom_sort"""
    assert custom_sort('Г') == ('Г', 0), "Обычная буква должна возвращаться без изменений"
    assert custom_sort('Ё') == ('Е', 1), "Буква Ё должна преобразовываться в Е с флагом 1"
    assert custom_sort('Е') == ('Е', 0), "Буква Е должна возвращаться без изменений"
    assert custom_sort('A') == ('A', 0), "Латинские буквы должны обрабатываться корректно"


def test_to_file():
    """Тестовые случаи для функции to_file"""
    test_data = {'А': 10, 'Ё': 5, 'Б': 3}
    to_file(test_data)

    try:
        with open('beasts.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        expected = [['А', '10'], ['Б', '3'], ['Ё', '5']]
        assert rows == expected, "Данные в файле не соответствуют ожидаемым"
    finally:
        import os
        if os.path.exists('beasts.csv'):
            os.remove('beasts.csv')


# Вспомогательные классы для мокирования
class MockPage:
    def __init__(self, name):
        self.name = name


class MockCategory:
    def __init__(self, pages):
        self.pages = pages

    def __iter__(self):
        return iter([MockPage(name) for name in self.pages])


class MockSite:
    def __init__(self, category_pages):
        self.categories = {"Животные по алфавиту": MockCategory(category_pages)}


def test_extract_animals():
    """Тестовый случай для функции extract_animals"""
    original_site = mwclient.Site
    test_pages = ['Аист', 'Барсук', 'Ёж', 'Енот', 'Wolf', '123Олень', '', 'Ягуар']
    mwclient.Site = lambda x: MockSite(test_pages)

    try:
        result = extract_animals()
        expected = {'А': 1, 'Б': 1, 'Ё': 1, 'Е': 1, 'Я': 1}
        assert result == expected, "Некорректный подсчет животных"
    finally:
        mwclient.Site = original_site


if __name__ == "__main__":
    test_custom_sort()
    test_to_file()
    test_extract_animals()
    print("Все тесты успешно пройдены!")
