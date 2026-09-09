from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        User,
        related_name='followers',
        blank=True
    )

    def _str_(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    def _str_(self):
        return self.content[:50]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.content[:50]
class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='following_relations',
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        User,
        related_name='follower_relations',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.follower.username} follows {self.following.username}"