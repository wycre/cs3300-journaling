import os
import time

from django.contrib.auth.models import User, Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from journal_app.models import Journal


class JournalFormTests(StaticLiveServerTestCase):
    """Test new and delete forms for Journals"""

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
        # Set up test data
        Group.objects.create(name='user')
        self.user = User.objects.create_user(username='testuser', email='testemail@example.com')
        self.user.groups.add(Group.objects.get(name='user'))
        self.user.set_password('testpass1')
        self.user.save()

        self.wait = WebDriverWait(self.driver, 10)

        self.test_image = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../assets", "test_image.jpg")
        )

        # Login the webdriver to allow forms to work
        self.login()

    def tearDown(self):
        # Clean up test data
        self.user.delete()


    def test_new_journal(self):
        """Test creation of new journal"""
        self.driver.get(self.live_server_url + '/journal/new')
        self.wait.until(lambda condition: self.driver.current_url == self.live_server_url + '/journal/new')

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
        journal_icon.send_keys(self.test_image)

        # Submit form
        submit.send_keys(Keys.RETURN)
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(lambda condition: self.driver.current_url != self.live_server_url + '/journal/new')

        # Test Presence of new journal
        assert 'Test Journal Alpha' in self.driver.page_source
        assert 'John Doe III' in self.driver.page_source
        assert 'Memo Field' in self.driver.page_source
        assert 'Newlines Supported' in self.driver.page_source
        assert 'defaults/journal_icon.svg' not in self.driver.page_source

    def test_delete_journal(self):
        """Test deletion of journal"""
        Journal.objects.create(title="Test Journal Beta", author_name="John Doe IV", memo="Memo",
                               user=User.objects.get(username='testuser'))

        self.driver.get(self.live_server_url + '/journal/delete?id=1')

        self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div/input').send_keys(Keys.ENTER)

        assert 'Test Journal Alpha' not in self.driver.page_source

    def test_edit_journal(self):
        """Test editing the journal"""
        journal = Journal.objects.create(title="Test Journal Beta", author_name="John Doe IV", memo="Memo",
                                         is_public=True, user=User.objects.get(username='testuser'))

        self.driver.get(self.live_server_url + '/journal/edit?id=' + str(journal.id))
        self.wait.until(lambda condition: self.driver.current_url == self.live_server_url + '/journal/edit?id=' + str(journal.id))

        journal_title = self.driver.find_element(By.CSS_SELECTOR, '#title')
        journal_author = self.driver.find_element(By.CSS_SELECTOR, '#author_name')
        journal_memo = self.driver.find_element(By.CSS_SELECTOR, '#memo')
        journal_is_public = self.driver.find_element(By.CSS_SELECTOR, '#is_public')
        submit = self.driver.find_element(By.CSS_SELECTOR, '#submit')

        journal_title.clear()
        journal_author.clear()
        journal_memo.clear()

        journal_title.send_keys('Test Journal Charlie')
        journal_author.send_keys('John Doe V')
        journal_memo.send_keys('Memo 2')
        journal_is_public.click()

        submit.send_keys(Keys.RETURN)

        self.wait.until(lambda condition: self.driver.current_url != self.live_server_url + '/journal/edit?id=' + str(journal.id))

        assert 'Test Journal Charlie' in self.driver.page_source
        assert 'John Doe V' in self.driver.page_source
        assert 'Memo 2' in self.driver.page_source
        assert Journal.objects.get(id=journal.id).is_public is False
