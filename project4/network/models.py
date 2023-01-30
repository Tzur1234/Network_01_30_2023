from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follow_others = models.ManyToManyField('User', related_name='follow_me', null=True, blank=True)
    img_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='posts_set')
    date = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    users_gave_like = models.ManyToManyField('User', related_name='posts_likes', null=True)

    # return a Post in a dict
    def serialize(self, user):
      
        return {
            "username": self.user.username,
            "post_id": self.id,
            "user_id": self.user.id,
            "postowner": user == self.user,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content,
            "likes": self.likes,
            "user_gave_like": user in self.users_gave_like.all()
        }


    def __str__(self):
        return f"(From {self.user}): {self.content}"
