from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import openpyxl

# Укажите абсолютный путь к chromedriver (замените на свой путь)
chrome_driver_path = 'D:/chromedriver-win64/chromedriver.exe'

# Создаем сервис для драйвера Chrome
service = Service(chrome_driver_path)

# Создаем опции для браузера Chrome
options = Options()

# Создаем экземпляр драйвера Chrome с указанным путем и опциями
driver = webdriver.Chrome(service=service, options=options)

try:
    # Открытие браузера и переход на страницу Codeforces
    driver.get("https://codeforces.com/enter?back=%2F")

    # Используем WebDriverWait для ожидания появления элементов
    wait = WebDriverWait(driver, 10)

    # Ввод логина и пароля
    handle = wait.until(EC.presence_of_element_located((By.ID, "handleOrEmail")))
    password = wait.until(EC.presence_of_element_located((By.ID, "password")))

    handle.send_keys("ulug.baxa.ru@yandex.ru")
    password.send_keys("c-&LidhjZn,vj6C")

    # Клик по кнопке отправки формы
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
    submit_button.click()

    # Даем немного времени для загрузки страницы после входа
    time.sleep(5)

    # Печать текущего URL для отладки
    print("Current URL after login:", driver.current_url)

    # Первый URL с результатами
    results_url_1 = "https://codeforces.com/group/x7EpYPdPGy/contest/520596/standings/groupmates/true/page/1"
    driver.get(results_url_1)

    # Печать текущего URL для отладки после перехода
    print("Current URL after navigating to contest standings page 1:", driver.current_url)

    # Ожидание загрузки страницы результатов
    time.sleep(5)

    # Получаем содержимое страницы
    page_content_1 = driver.page_source

    # Используем BeautifulSoup для парсинга страницы
    soup_1 = BeautifulSoup(page_content_1, 'html.parser')

    # Извлечение таблицы результатов
    table_1 = soup_1.find('table', {'class': 'standings'})

    # Извлечение строк таблицы
    rows_1 = table_1.find_all('tr')

    # Список для хранения данных
    data_1 = []

    # Извлечение данных из строк таблицы
    for row in rows_1[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data_1.append(cols)

    # Вывод первых нескольких строк данных для проверки
    print("First few rows of data from page 1:")
    for i in range(min(5, len(data_1))):  # Печатаем первые 5 строк данных или все, если их меньше
        print(data_1[i])

    # Второй URL с результатами (измените URL на фактический)
    results_url_2 = "https://codeforces.com/group/x7EpYPdPGy/contest/520596/standings/participant/181227699/page/2"
    driver.get(results_url_2)

    # Печать текущего URL для отладки после перехода
    print("Current URL after navigating to contest standings page 2:", driver.current_url)

    # Ожидание загрузки страницы результатов
    time.sleep(5)

    # Получаем содержимое страницы
    page_content_2 = driver.page_source

    # Используем BeautifulSoup для парсинга страницы
    soup_2 = BeautifulSoup(page_content_2, 'html.parser')

    # Извлечение таблицы результатов
    table_2 = soup_2.find('table', {'class': 'standings'})

    # Извлечение строк таблицы
    rows_2 = table_2.find_all('tr')

    # Список для хранения данных со второй страницы
    data_2 = []

    # Извлечение данных из строк таблицы
    for row in rows_2[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data_2.append(cols)

    # Вывод первых нескольких строк данных для проверки
    print("First few rows of data from page 2:")
    for i in range(min(5, len(data_2))):  # Печатаем первые 5 строк данных или все, если их меньше
        print(data_2[i])

    # Объединение данных из двух страниц в один список
    combined_data = data_1 + data_2

    # Создание DataFrame
    df = pd.DataFrame(combined_data, columns=['Rank', 'Who', 'Solved', 'Penalty'])

    # Запись DataFrame в файл Excel
    df.to_excel('results.xlsx', index=False)
    # w
finally:
    # Закрытие браузера в любом случае
    driver.quit()
