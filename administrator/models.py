from django.db import models
from accounts.models import *
from posts.models import *


class AdministratorPostSession(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_session_data")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name="post_profile_session_data")
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return "Session"
    
    