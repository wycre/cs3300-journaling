import os.path
import random

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from journal_app.models import Journal


# Create your tests here.
class JournalLoginTest(StaticLiveServerTestCase):
    """Test new and delete forms for Journals"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_form(self):
        # Initialize Test Values
        test_image = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../assets", "test_image.jpg")
        )

        # Run Registration
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
        email.send_keys("testemail" + rand_num + "@email.com")
        password1.send_keys("testpass1")
        password2.send_keys("testpass1")

        print("User Number: " + rand_num)

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

        # Make a new Journal
        self.driver.get('http://localhost:8000/journal/new')
        wait.until(lambda condition: self.driver.current_url == 'http://localhost:8000/journal/new')

        # Get Form Fields
        journal_title = self.driver.find_element(By.CSS_SELECTOR, '#title')
        journal_author = self.driver.find_element(By.CSS_SELECTOR, '#author_name')
        journal_memo = self.driver.find_element(By.CSS_SELECTOR, '#memo')
        journal_is_public = self.driver.find_element(By.CSS_SELECTOR, '#is_public')
        journal_icon = self.driver.find_element(By.CSS_SELECTOR, '#journal_icon')
        submit = self.driver.find_element(By.CSS_SELECTOR, '#submit')

        # Fill Form
        journal_title.send_keys('Test Journal Alpha')
        journal_author.send_keys('John Doe III')
        journal_memo.send_keys('Memo Field \n \n Newlines Supported')
        journal_is_public.send_keys(Keys.SPACE)
        journal_icon.send_keys(test_image)

        # Submit form
        submit.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda condition: self.driver.current_url != 'http://localhost:8000/journal/new')

        # Test Presence of new journal
        assert 'Test Journal Alpha' in self.driver.page_source
        assert 'John Doe III' in self.driver.page_source
        assert 'Memo Field' in self.driver.page_source
        assert 'Newlines Supported' in self.driver.page_source
        assert 'defaults/journal_icon.svg' not in self.driver.page_source

        # Test Delete
        # Open Edit Form
        self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div[2]/a').send_keys(Keys.ENTER)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda condition: 'Edit Journal Details' in self.driver.page_source)

        # Open Delete Form
        self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div[2]/a[2]').send_keys(Keys.ENTER)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda condition: 'This action cannot be undone.' in self.driver.page_source)

        self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div/input').send_keys(Keys.ENTER)

        assert 'Test Journal Alpha' not in self.driver.page_source




