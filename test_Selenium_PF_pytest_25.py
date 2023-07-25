from settings import valid_email, valid_password
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_my_pets(driver):
    # Проверка всех питомцев пользователя на наличие имени, вида и возраста.
    # Устанавливаем неявное ожидание
    driver.implicitly_wait(10)

    driver.maximize_window()
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, "pass").send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # нажимаем кнопку "мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    images = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    age = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert age[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
    print('У всех питомцев пользователя имеется имя, вид и возраст.')

    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(driver, 5)

    ## Тест, который проверяет, что на странице со списком питомцев пользователя:
    # Присутствуют все питомцы.
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    # Сохраняем в переменную ststistics элементы статистики

    statistic = driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    # Сохраняем в переменную pets элементы карточек питомцев
    pets = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    # Получаем количество карточек питомцев
    number_of_pets = len(pets)
    print(f'Тест1 количество моих питомцев: {number_of_pets}')
    # Проверяем что количество питомцев из статистики совпадает с количеством карточек питомцев
    assert number == number_of_pets
    print(f'Тест2 Присутствуют все питомцы: {number == number_of_pets}')

    # Написать тест, который проверяет, что на странице со списком питомцев пользователя:
    # Хотя бы у половины питомцев есть фото.
    # Сохраняем в переменную images элементы с атрибутом img
    images = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')
    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    # Находим половину от количества питомцев
    half = number // 2
    # Находим количество питомцев с фотографией
    number_а_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_а_photos += 1
    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    assert number_а_photos >= half
    print(f'Тест3 Количество питомцев с фото: {number_а_photos}')
    print(f'Тест4 Половина от числа питомцев: {half}')

    # Написать тест, который проверяет, что на странице со списком питомцев пользователя:
    # У всех питомцев есть имя, возраст и порода.

    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Сохраняем в переменную pet_data элементы с данными о питомцах
    pet_data = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу. Находим количество элементов в получившемся списке и сравниваем их
    # с ожидаемым результатом
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        result = len(split_data_pet)
        assert result >= 3
    print(f'Тест5 Все {len(pet_data)} Питомцы имеют имя, возраст и породу')

    # Написать тест, который проверяет, что на странице со списком питомцев пользователя:
    # У всех питомцев разные имена

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу. Выбираем имена и добавляем их в список pets_name.
    pets_name = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_name.append(split_data_pet[0])

    # Перебираем имена и если имя повторяется то прибавляем к счетчику r единицу.
    # Проверяем, если r == 0 то повторяющихся имен нет.
    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
    assert r == 0
    print(f'Тест6 Количество повторений: {r}')

    # Написать тест, который проверяет, что на странице со списком питомцев пользователя:
    # В списке нет повторяющихся питомцев
    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем пробелом
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)

    # Склеиваем имя, возраст и породу, добавляем в строку и между ними вставляем пробел
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0
    print('Тест7 В списке нет повторяющихся питомцев')
