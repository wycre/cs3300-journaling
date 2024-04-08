import os.path

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from journal_app.models import Journal


# Create your tests here.
class JournalFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_form(self):
        # Initialize Test Values
        test_image = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "tests", "test_image.jpg")
        )

        # Initialize Selenium
        self.driver.get('http://localhost:8000/journal/new')

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

    def tearDown(self):
        # Delete Test Journal
        self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div[2]/a').send_keys(Keys.ENTER)

        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda condition: 'Edit Journal Details' in self.driver.page_source)

        self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div[2]/a[2]').send_keys(Keys.ENTER)

        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda condition: 'This action cannot be undone.' in self.driver.page_source)

        self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div/input').send_keys(Keys.ENTER)
