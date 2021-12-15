from django.http import response
from django.test import TestCase, Client
from .models import User, Post
from django.urls import reverse
import json
# Create your tests here.

class NetworkTestCases(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(username="Test1", email="example@gmail.com", password="ABCDE")
        user2 = User.objects.create_user(username="Test2", email="example2@gmail.com", password="ABCDE")
        user3 = User.objects.create_user(username="Test3", email="example3@gmail.com", password="ABCDE")
        Post.objects.create(author = user1, content = "This is 1st test post")
        Post.objects.create(author = user2, content = "This is 2nd test post")
        Post.objects.create(author = user2, content = "This is 3rd test post")
        self.client = Client()
        self.client.login(username="Test1", password="ABCDE")
    
    def test_index_get(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(len(response.context["postLikes"]), 3)
        self.assertEqual(response.status_code, 200)

    def test_index_post_form(self):
        response = self.client.post(reverse("index"), {"content": "A test post"})
        new_get_response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(new_get_response.context["postLikes"]), 4)
    
    def test_profile(self):
        user = User.objects.get(username="Test1")
        response = self.client.get(f"/profile/{user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["postLikes"]), 1)
    
    def test_following(self):
        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")
        user1.follow_user(user2)
        response = self.client.get(reverse("following"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["postLikes"]), 2)
    
    def test_follow(self):
        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")
        bodyData = json.dumps({"profileId": user2.id})
        response = self.client.post(path=reverse("follow"), data=bodyData, content_type="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user1.does_follow(user2))
    
    def test_like(self):
        user1 = User.objects.get(username="Test1")        
        post1 = Post.objects.get(content="This is 1st test post")
        bodyData = json.dumps({"postId": post1.id})
        response = self.client.post(path=reverse("like"), data=bodyData, content_type="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user1.does_like(post1))
    
    def test_save(self):
        post1 = Post.objects.get(content="This is 1st test post")
        bodyData = json.dumps({"postId": post1.id, "content": "This is new content"})
        response = self.client.put(path=reverse("save"), data=bodyData, content_type="json")
        newPost = Post.objects.get(id = post1.id)
        self.assertEqual(newPost.content, "This is new content")
        self.assertEqual(response.status_code, 200)

    def test_does_like(self):
        user1 = User.objects.get(username="Test1")
        post1 = Post.objects.get(content="This is 1st test post")
        post2 = Post.objects.get(content="This is 2nd test post")
        user1.like_post(post1)
        user1_likes_post1 = user1.does_like(post1)
        user1_likes_post2 = user1.does_like(post2)
        self.assertTrue(user1_likes_post1)
        self.assertFalse(user1_likes_post2)
    
    def test_does_follow(self):
        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")
        user3 = User.objects.get(username="Test3")
        user1.follow_user(user2)
        user1_follows_user2 = user1.does_follow(user2)
        user1_follows_user3 = user1.does_follow(user3)
        
        self.assertTrue(user1_follows_user2)
        self.assertFalse(user1_follows_user3)
    
    def test_unfollow(self):
        user1 = User.objects.get(username="Test1")
        user2 = User.objects.get(username="Test2")
        user1.follow_user(user2)
        user1.unfollow(user2)
        user1_follows_user2 = user1.does_follow(user2)

        self.assertFalse(user1_follows_user2)