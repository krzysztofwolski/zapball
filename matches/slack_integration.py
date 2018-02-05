from . import JOIN_MATCH_ACTION
from .models import Match
from .utils import get_match_users
from slack.utils import (
    is_slack_token_valid, get_or_create_slack_user, format_user_mention)


def match_description_message(match: Match) -> dict:
    users = get_match_users(match)
    lobby_players = ', '.join(
        [format_user_mention(u.slackuser) for u in users])

    response = {
        "response_type": "in_channel",
        "text": "Created new match",
        "attachments": [
            {
                "text": f"Lobby: {lobby_players}",
                "callback_id": f"{match.pk}",
                "actions": [
                    {
                        "name": "action",
                        "text": "Join",
                        "type": "button",
                        "value": JOIN_MATCH_ACTION
                    }
                ]
            }
        ]
    }

    return response


def match_started_message(match: Match) -> dict:
    teams = match.teams.all()

    team_messages = []
    for team in teams:
        users = [p.user for p in team.players.all()]
        player_list = ', '.join(
            [
                format_user_mention(u.slackuser)
                for u in users
            ]
        )

        team_messages.append(
            {
                "text": player_list,
                "color": "#3AA3E3",
                "attachment_type": "default"
            }
        )

    response = {
        "text": "Match started!",
        "attachments": team_messages
    }

    return response
