from typing import Tuple, List
import random

from django.contrib.auth.models import User

from .models import Match, MatchPlayer, Game, MatchTeam


def create_match(game: Game, user: User, msg: str='') -> Match:
    """Create match and join its createor into it"""
    match, teams = prepare_match(game, msg)
    join_random_team(user, teams)
    return match


def prepare_match(game: Game, msg: str='') -> Tuple[Match, List[MatchTeam]]:
    """Prepare match objects"""
    match = Match.objects.create(message=msg, game=game)

    teams = [
        MatchTeam.objects.create(match=match)
        for i in range(game.teams)]

    return match, teams


def join_match(match: Match, user: User) -> Tuple[bool, str]:
    teams = list(MatchTeam.objects.filter(match=match))
    return join_random_team(user, teams)


def get_match_users(match: Match) -> List[User]:
    teams = list(MatchTeam.objects.filter(match=match))
    users = get_users_from_teams(teams)
    return users


def is_team_full(team: MatchTeam):
    return len(team.players.all()) == team.match.game.players_per_team


def is_match_full(match: Match):
    return all(
        [
            is_team_full(team)
            for team in match.teams.all()
        ]
    )


def get_users_from_teams(teams: List[MatchTeam]) -> List[User]:
    users = []  # type: List[User]
    for team in teams:
        users += [
            match_player.user
            for match_player in team.players.all()]

    return users


def join_random_team(user: User, teams: List[MatchTeam]) -> Tuple[bool, str]:
    """Join given user to one of provided teams. Returns tuple with boolean
    describing operation success and message"""

    # check if player already joined
    if user in get_users_from_teams(teams):
        return False, 'already joined'

    # check for available teams
    available_teams = list(filter(lambda x: not is_team_full(x), teams))

    if len(available_teams) == 0:
        return False, 'no free spots'

    team = random.choice(available_teams)
    MatchPlayer.objects.create(team=team, user=user)
    return True, 'success'
