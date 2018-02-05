from django.db import models
from django.contrib.auth.models import User


class SlackUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slack_team = models.CharField(max_length=250)
    slack_user_id = models.CharField(max_length=250)
    slack_username = models.CharField(max_length=250)

    class Meta:
        unique_together = (
            'slack_team', 'slack_user_id', 'slack_username')
