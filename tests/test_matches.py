from pytest import fixture

from matches.models import Game, MatchTeam, MatchPlayer
from matches import utils


@fixture
def foosball_game(db):
    return Game.objects.create(
        name='foosball', teams=2, players_per_team=2)


@fixture
def user_a(django_user_model):
    return django_user_model.objects.create(
        username='playera',
        email='playera@example.com')


@fixture
def user_b(django_user_model):
    return django_user_model.objects.create(
        username='playerb',
        email='playerb@example.com')


@fixture
def user_c(django_user_model):
    return django_user_model.objects.create(
        username='playerc',
        email='playerc@example.com')


@fixture
def user_d(django_user_model):
    return django_user_model.objects.create(
        username='playerd',
        email='playerd@example.com')


@fixture
def user_e(django_user_model):
    return django_user_model.objects.create(
        username='playere',
        email='playere@example.com')


def test_prepare_match(foosball_game):
    match, teams = utils.prepare_match(foosball_game)
    assert match
    assert len(teams) == 2


def test_is_team_full(foosball_game, user_a, user_b):
    # foosball game can have 2 players in a team
    match, teams = utils.prepare_match(foosball_game)
    team = teams[0]

    # no players in team
    assert not utils.is_team_full(team)

    # one player
    MatchPlayer.objects.create(team=team, user=user_a)
    assert not utils.is_team_full(team)

    # 2 players = full team
    MatchPlayer.objects.create(team=team, user=user_b)
    assert utils.is_team_full(team)


def test_join_random_team(
        foosball_game, user_a, user_b, user_c, user_d, user_e):
    # foosball game can be joined by 4 players.
    # They will be splitted into 2 teams.
    users = [user_a, user_b, user_c, user_d]

    # check if 4 users successfully joins any team
    match, teams = utils.prepare_match(foosball_game)
    team_a, team_b = teams

    for user in users:
        assert utils.join_random_team(user, teams)
        assert (team_a.players.filter(user=user).exists() or
                team_b.players.filter(user=user).exists())

    # 5th player should not be able to join
    assert not utils.join_random_team(user_e, teams)

    # players should not be able to join match multiple times
    assert not utils.join_random_team(user_a, teams)
