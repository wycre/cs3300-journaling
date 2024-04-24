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
class PostNewDeleteTest(LiveServerTestCase):
    """Test new and delete forms for Posts"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_forms(self):
        # Run Registration
        # Make test account
        self.driver.get('http://localhost:8000/profile/register')

        # Get Form Fields
        username = self.driver.find_element(By.XPATH, '//*[@id="id_username"]')
        email = self.driver.find_element(By.XPATH, '//*[@id="id_email"]')
        password1 = self.driver.find_element(By.XPATH, '//*[@id="id_password1"]')
        password2 = self.driver.find_element(By.XPATH, '//*[@id="id_password2"]')
        submit = self.driver.find_element(By.CSS_SELECTOR, '.container > form:nth-child(2) > input:nth-child(8)')

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
        username = self.driver.find_element(By.XPATH, '//*[@id="id_username"]')
        password1 = self.driver.find_element(By.XPATH, '//*[@id="id_password"]')
        submit = self.driver.find_element(By.CSS_SELECTOR, '.container > form:nth-child(2) > input:nth-child(3)')

        username.send_keys("testuser" + rand_num)
        password1.send_keys("testpass1")

        submit.send_keys(Keys.RETURN)
        wait.until(lambda condition: self.driver.current_url == 'http://localhost:8000/')


        # Make new post
        self.driver.get('http://localhost:8000/post/new?id=3')
        wait.until(lambda condition: 'New Post' in self.driver.page_source)

        title = self.driver.find_element(By.XPATH, '//*[@id="title"]')
        body = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/div[1]/trix-editor')
        submit = self.driver.find_element(By.XPATH, '//*[@id="submit"]')

        title.send_keys("Test Post Alhpa")
        body.send_keys("Test Body \n \n Newlines")
        body.send_keys(Keys.CONTROL, "i")
        body.send_keys("Italic Text as well")

        submit.send_keys(Keys.RETURN)
        wait.until(lambda condition: "Test Post Alpha" in self.driver.page_source)

        # Verify Post
        assert "Test Post Alpha" in self.driver.page_source
        assert "<em>Italic" in self.driver.page_source

        # Delete Post
        temp = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/div/a')
        temp.send_keys(Keys.RETURN)
        wait.until(lambda condition: "Edit Post" in self.driver.page_source)

        temp = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/div[2]/a[2]')
        temp.send_keys(Keys.RETURN)
        wait.until(lambda condition: "This action cannot be undone." in self.driver.page_source)

        temp = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/div/input')
        temp.send_keys(Keys.RETURN)
        wait.until(lambda condition: self.driver.current_url == 'http://localhost:8000/')

        self.driver.get('http://localhost:8000/journal?id=3')
        wait.until(lambda condition: self.driver.current_url == 'http://localhost:8000/journal?id=3')

        assert "Test Post Alpha" not in self.driver.page_source




