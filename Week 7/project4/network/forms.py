from django.forms import ModelForm
from .models import Post, User

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]