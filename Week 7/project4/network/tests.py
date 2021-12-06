from django.test import TestCase, Client
from .models import User, Post
from django.urls import reverse
# Create your tests here.

class NetworkTestCases(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(username="Test1", email="example@gmail.com", password="ABCDE")
        user2 = User.objects.create_user(username="Test2", email="example2@gmail.com", password="ABCDE")
        post1 = Post.objects.create(author = user1, content = "This is 1st test post")
        post2 = Post.objects.create(author = user2, content = "This is 2nd test post")
        post3 = Post.objects.create(author = user2, content = "This is 3rd test post")
        self.client = Client()
        self.index_url = reverse("index")
        self.client.login(username="Test1", password="ABCDE")
    
    def test_index_get(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)

    def test_index_post_form(self):
        response = self.client.post(self.index_url, {"content": "A test post"})
        self.assertEqual(response.status_code, 302)