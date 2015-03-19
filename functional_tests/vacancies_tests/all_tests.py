from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
import unittest
from django.test import LiveServerTestCase
from unittest import skip
from selenium.webdriver.support.ui import Select

class VacancyTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def test_user_add_new_vacancy(self):
        #Пользователь переходит на страницу с вакансиями
        self.browser.get(self.live_server_url+'/vacancies/add')

        #Пользователь заполняет поля и нажимает кнопку Добавить
        position = Select(self.browser.find_element_by_id('position'))
        salary = self.browser.find_element_by_id('salary')
        end_date = self.browser.find_element_by_id('end_date')
        description = self.browser.find_element_by_id('description')
        department = Select(self.browser.find_element_by_id('department'))




