from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import User

from .models import SlackUser


def is_slack_token_valid(token: str) -> bool:
    return token == settings.SLACK_VERIFICATION_TOKEN


def format_user_mention(user: SlackUser) -> str:
    return f'<@{user.slack_user_id}|{user.slack_username}>'


def get_or_create_slack_user(
        team: str, user_id: str, username: str
        ) -> SlackUser:

    slack_user = SlackUser.objects.filter(
        slack_team=team, slack_user_id=user_id, slack_username=username
    ).first()

    # existing user
    if slack_user is not None:
        return slack_user

    user, _ = User.objects.get_or_create(
        username=f'{username}{user_id}',
        email=f'{username}@{team}.slack')

    slack_user = SlackUser.objects.create(
        user=user,
        slack_team=team,
        slack_user_id=user_id,
        slack_username=username)

    return slack_user
