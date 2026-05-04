from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # No profile_pics was created yet
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    # following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    # def follow(self, user):
    #     if user != self:
    #         self.following.add(user)
    
    # def unfollow(self, user):
    #     if user != self:
    #         self.following.remove(user)

    def __str__(self):
        return self.username
    
class UserFollowing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following_relations',
        on_delete=models.CASCADE
    )
    following_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='follower_relations',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following_user')

    def __str__(self):
        return f"{self.user} follows {self.following_user}"
