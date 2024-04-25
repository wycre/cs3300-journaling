import time

from django.contrib.auth.models import User, Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, LiveServerTestCase, override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


# Create your tests here.
class AuthenticationTests(StaticLiveServerTestCase):
    """Test authentication forms"""

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
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        pass

    def test_registration(self):
        """Test User Registration"""
        self.driver.get(self.live_server_url + '/profile/register')
        self.wait.until(lambda condition: '/profile/register' in self.driver.current_url)

        # Get Form Fields
        username = self.driver.find_element(By.XPATH, '//*[@id="id_username"]')
        email = self.driver.find_element(By.XPATH, '//*[@id="id_email"]')
        password1 = self.driver.find_element(By.XPATH, '//*[@id="id_password1"]')
        password2 = self.driver.find_element(By.XPATH, '//*[@id="id_password2"]')
        submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/form/input[6]')

        # Fill Form
        username.send_keys("testuser")
        email.send_keys("testuser@email.com")
        password1.send_keys("testpass1")
        password2.send_keys("testpass1")

        # Submit form
        submit.send_keys(Keys.RETURN)
        self.wait.until(lambda condition: self.driver.current_url == self.live_server_url + '/profile/login/')

        users = User.objects.all()
        assert "testuser" not in users

    def test_login_logout(self):
        """Test User Login"""
        self.driver.get(self.live_server_url + '/profile/login')
        self.wait.until(lambda condition: '/profile/login' in self.driver.current_url)

        if User.objects.filter(username='testuser').count() == 0:
            user = User.objects.create(username='testuser', email='testuser@email.com')
            user.set_password('testpass1')
            user.save()

        # Log In
        username = self.driver.find_element(By.XPATH, '//*[@id="username"]')
        password1 = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/form/input[4]')

        username.send_keys("testuser")
        password1.send_keys("testpass1")

        submit.send_keys(Keys.RETURN)
        self.wait.until(lambda condition: "Welcome" in self.driver.page_source)

        # Test user is logged in
        assert "Logout testuser" in self.driver.page_source

        # Logout user
        logout = self.driver.find_element(By.XPATH, '/html/body/div[1]/nav/div/div/div/div/a[4]')
        logout.send_keys(Keys.RETURN)

        time.sleep(1)
        assert r'<a class="nav-link" href="/profile/login/?next=/?">Login</a>' in self.driver.page_source
