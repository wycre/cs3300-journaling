import os.path
import random
import time

from django.contrib.auth.models import User, Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, LiveServerTestCase, override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from journal_app.models import Journal, Post


# Create your tests here.
class PostFormTests(StaticLiveServerTestCase):
    """Test Post Form Integration"""

    def login(self):
        """Logs the webdriver into the test user"""
        self.driver.get(self.live_server_url + '/profile/login')
        username = self.driver.find_element(By.XPATH, '//*[@id="username"]')
        password1 = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/input[4]')

        username.send_keys("testuser")
        password1.send_keys("testpass1")

        submit.send_keys(Keys.RETURN)
        self.wait.until(lambda condition: self.driver.current_url == self.live_server_url + '/')


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        Group.objects.create(name='user')
        self.user = User.objects.create(username='testuser', email='testuser@email.com')
        self.user.set_password('testpass1')
        self.user.groups.add(Group.objects.get(name='user'))
        self.user.save()

        self.journal = Journal.objects.create(title='Test Journal', author_name="John Doe", memo="Memo", user=self.user,
                                              is_public=True)

        self.wait = WebDriverWait(self.driver, 10)

        self.login()

    def test_new_post(self):
        """Test creating a new post"""
        self.driver.get(self.live_server_url + '/post/new?id='+str(self.journal.id))
        self.wait.until(lambda condition: '/post/new' in self.driver.current_url)

        # Fill New Post Form
        title = self.driver.find_element(By.XPATH, '//*[@id="title"]')
        body = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/div[1]/trix-editor')
        submit = self.driver.find_element(By.XPATH, '//*[@id="submit"]')

        title.send_keys("Test Post Alpha")
        body.send_keys("Test Body\n")
        body.send_keys(Keys.CONTROL, 'b')
        body.send_keys("Bold Text")
        submit.send_keys(Keys.ENTER)

        self.wait.until(lambda condition: '/post?' in self.driver.current_url)

        assert "Test Post Alpha" in self.driver.page_source
        assert "Test Body" in self.driver.page_source
        assert "<strong>Bold Text</strong>" in self.driver.page_source

    def test_edit_post(self):
        """Test editing a post"""
        post = Post.objects.create(title='Test Post Alpha', content="Content", journal=self.journal)

        self.driver.get(self.live_server_url + '/post/edit?p='+str(post.id))
        self.wait.until(lambda condition: '/post/edit' in self.driver.current_url)

        title = self.driver.find_element(By.XPATH, '//*[@id="title"]')
        body = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/div[1]/trix-editor')
        submit = self.driver.find_element(By.XPATH, '//*[@id="submit"]')

        title.clear()
        title.send_keys("Test Post Beta")
        body.send_keys("Body Edit\n")
        body.send_keys(Keys.CONTROL, 'i')
        body.send_keys("Italic Text")
        submit.send_keys(Keys.ENTER)

        self.wait.until(lambda condition: '/post?' in self.driver.current_url)

        assert "Test Post Beta" in self.driver.page_source
        assert "Body Edit" in self.driver.page_source
        assert "<em>Italic Text</em>" in self.driver.page_source

    def test_delete_post(self):
        """Test deleting a post"""
        post = Post.objects.create(title='Test Post Alpha', content="Content", journal=self.journal)

        self.driver.get(self.live_server_url + '/post/delete?p=' + str(post.id))
        self.wait.until(lambda condition: '/post/delete' in self.driver.current_url)

        submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/div/input')

        submit.send_keys(Keys.ENTER)

        self.wait.until(lambda condition: '/public' in self.driver.current_url)
        assert post not in Post.objects.all()




