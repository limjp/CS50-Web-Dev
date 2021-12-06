from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    following = models.ManyToManyField("self", through="Following", symmetrical=False)
    date_created = models.DateField(auto_now_add=True)

    def follow(self, user):
        Following.objects.create(
            follower_id = self,
            followered_id = user
        )
        return

    def does_follow(self, user):
        try:
            Following.objects.get(
                follower_id = self,
                followered_id = user
            )
            return True
        except:
            return False
    
    def unfollow(self, user):
        Following.objects.filter(
            follower_id = self,
            followered_id = user
        ).delete()
        return

    def like_post(self, post):
        Like.objects.create(
        user_id = self,
        post_id = post
        )
        return

    def does_like(self, post):
        try:
            Like.objects.get(
                user_id = self,
                post_id = post
            )
            return True
        except:
            return False
    
    def unlike_post(self, post):
        Like.objects.filter(
            user_id = self,
            post_id = post
        ).delete()
        return

    def create_post(self, content):
        Post.objects.create(
            author = self,
            content = content
        )

    def __str__(self) -> str:
        return f"{self.id}, {self.username}"

class Following(models.Model):
    follower_id = models.ForeignKey(User, related_name="followers", on_delete=CASCADE)
    followered_id = models.ForeignKey(User, related_name="follow", on_delete=CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Follower: {self.follower_id}, Following: {self.followered_id}"

class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=CASCADE)
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, through="Like", blank=True, null=True, related_name="posts_liked")

    def __str__(self) -> str:
        return f"{self.id}, {self.author}, {self.content}"

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    post_id = models.ForeignKey(Post, on_delete=CASCADE)
    date_liked = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_id}, {self.post_id}"