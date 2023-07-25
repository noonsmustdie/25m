import pytest as pytest
from selenium import webdriver


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome("C:\Selenium\chromedriver.exe")
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()
