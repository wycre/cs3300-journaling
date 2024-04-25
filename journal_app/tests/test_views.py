from urllib.parse import urlencode

from django.test import Client, TestCase

from journal_app.models import Journal, Post
from django.contrib.auth.models import User, Group


class ViewTest(TestCase):
    """Tests all the views"""

    def setUp(self):
        Group.objects.create(name='user')
        self.user = User.objects.create(username='test', email="test@email.com")
        self.user.set_password('password')
        self.user.groups.add(Group.objects.get(name='user'))
        self.user.save()
        self.journal = Journal.objects.create(title='Test Journal', author_name="John Doe", memo="Description",
                                              is_public=True, user=self.user)
        self.post = Post.objects.create(title='Test Post', content="Description", journal=self.journal)

    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public/homepage.html')

    def test_list_journals(self):
        client = Client()
        response = client.get('/public')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public/list_journals.html')

    def test_list_journals_own(self):
        client = Client()
        client.login(username='test', password='password')
        response = client.get('/profile/journals')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authed/list_journals_own.html')

    def test_detail_journal(self):
        client = Client()
        response = client.get('/journal?id=1')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public/detail_journal.html')

    def test_new_journal(self):
        client = Client()
        client.login(username='test', password='password')

        # Test GET
        response = client.get('/journal/new')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authed/forms/journal_create_form.html')

        # Test POST
        data = {'title': 'Test Journal Alpha', 'author_name': 'John Doe IV',
                'memo': 'Description Alpha', 'is_public': True}
        response = client.post('/journal/new', data)
        self.assertEqual(response.status_code, 302)
        response = client.get(response.url)  # GET redirect URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public/detail_journal.html')
        self.assertContains(response, 'Test Journal Alpha')
        self.assertContains(response, 'John Doe IV')
        self.assertContains(response, 'Description Alpha')

    def test_detail_post(self):
        client = Client()
        response = client.get('/post?p=1')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'public/detail_post.html')
