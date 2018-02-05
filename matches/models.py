from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=250)
    teams = models.PositiveIntegerField()
    players_per_team = models.PositiveIntegerField()

    def __unicode__(self):
        return f'{self.name} game ({self.pk})'


class Match(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(
        to=Game, on_delete=models.CASCADE, related_name='matches')
    message = models.CharField(max_length=250, default='')
    finished = models.BooleanField(default=False)
    started = models.BooleanField(default=False)

    def __unicode__(self):
        return f'Match of {self.game} ({self.pk})'


class MatchTeam(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    match = models.ForeignKey(
        to=Match, on_delete=models.CASCADE, related_name='teams')
    won = models.NullBooleanField(default=None)


class MatchPlayer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(
        to=MatchTeam, on_delete=models.CASCADE, related_name='players')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __unicode__(self):
        return f'Player {self.user} ({self.pk})'
