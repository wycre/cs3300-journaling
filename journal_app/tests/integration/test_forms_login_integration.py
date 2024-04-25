import os.path
import random

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from journal_app.models import Journal


# Create your tests here.
class JournalFormTest(StaticLiveServerTestCase):
    """Test all forms related to Journals"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def test_form(self):
        # Make test account
        self.driver.get('http://localhost:8000/profile/register')

        # Get Form Fields
        username = self.driver.find_element(By.XPATH, '//*[@id="id_username"]')
        email = self.driver.find_element(By.XPATH, '//*[@id="id_email"]')
        password1 = self.driver.find_element(By.XPATH, '//*[@id="id_password1"]')
        password2 = self.driver.find_element(By.XPATH, '//*[@id="id_password2"]')
        submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/form/input[6]')


        # Fill Form
        rand_num = str(random.randint(1, 100))
        username.send_keys("testuser" + rand_num)
        email.send_keys("testemail"+rand_num+"@email.com")
        password1.send_keys("testpass1")
        password2.send_keys("testpass1")

        print("User Number: "+rand_num)

        # Submit form
        submit.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda condition: self.driver.current_url == 'http://localhost:8000/profile/login/')

        # Log In
        username = self.driver.find_element(By.XPATH, '//*[@id="username"]')
        password1 = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/input[4]')

        username.send_keys("testuser" + rand_num)
        password1.send_keys("testpass1")

        submit.send_keys(Keys.RETURN)
        wait.until(lambda condition: self.driver.current_url == 'http://localhost:8000/')

        # Test user is logged in
        assert "Logout testuser"+rand_num in self.driver.page_source


        # Logout user
        logout = self.driver.find_element(By.XPATH, '/html/body/div[1]/nav/div/div/div/div/a[4]')
        logout.send_keys(Keys.RETURN)

        wait.until(lambda condition: self.driver.current_url == 'http://localhost:8000/?')
        assert r'<a class="nav-link" href="/profile/login/?next=/?">Login</a>' in self.driver.page_source




