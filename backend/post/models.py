from django.db import models

from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.TextField(default='')
    description = models.TextField(default='')
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['published_at']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.title}"

    def author(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Tag(models.Model):
    post = models.ManyToManyField(Post, related_name='post_tag')
    tag_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['tag_name']

    def __str__(self):
        return self.tag_name


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='post_liked', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_liked', on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.first_name}. Author is {self.post.user.first_name} for post title {self.post.title}"

