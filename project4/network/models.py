from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pfp = models.ImageField(upload_to= "pfp/", blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical= False, related_name= "following")

    def __str__(self):
        return self.username

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete= models.CASCADE, related_name= "posts")
    likes = models.ManyToManyField("User", through = "Like",related_name= "liked")
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.poster.username}: {self.content[:30]}"
    class Meta:
        ordering = ["-time"]


class Comment(models.Model):
    commenter = models.ForeignKey("User", on_delete = models.CASCADE, related_name="comments")
    post = models.ForeignKey("Post", on_delete= models.CASCADE, related_name = "comments")
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["-time"]

class Like(models.Model):
    user = models.ForeignKey("User", related_name = "liked_posts", on_delete= models.CASCADE)
    post = models.ForeignKey("Post", related_name= "like_objects", on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "post")


    def __str__(self):
        return f"{self.user.username} liked post {self.post.id} at {self.time}"