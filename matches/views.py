import json
import requests

from django.http import (
    JsonResponse, HttpRequest, HttpResponseForbidden, HttpResponse)
from django.views.decorators.csrf import csrf_exempt

from slack.utils import is_slack_token_valid, get_or_create_slack_user
from .utils import create_match, join_match, get_match_users, is_match_full
from .models import Game, Match
from .slack_integration import match_description_message, match_started_message


@csrf_exempt
def start_match(request: HttpRequest) -> HttpResponse:
    if not is_slack_token_valid(request):
        return HttpResponseForbidden()
    # <QueryDict: {
    #     'token': ['ThXMxn996fFZSKae2e28yw5h'],
    #     'team_id': ['T02A70N2B'],
    #     'team_domain': ['mirumee'],
    #     'channel_id': ['C6W3BAE81'],
    #     'channel_name': ['test'],
    #     'user_id': ['U1Z5J6YB1'],
    #     'user_name': ['krzyh'],
    #     'command': ['/kick_me'],
    #     'text': [''],
    #     'response_url': ['https://hooks.slack.com/commands/T02A70N2B/309804181605/ffZglItCpzL7AnXY0kxhZrMk'],
    #     'trigger_id': ['310538834918.2347022079.04c1148fe39ff1c6493f8c23c8a5d04e']}>

    slack_user = get_or_create_slack_user(
        team=request.POST.get('team_domain'),
        user_id=request.POST.get('user_id'),
        username=request.POST.get('user_name'))

    game = Game.objects.first()
    match = create_match(game=game, user=slack_user.user)

    slack_message = match_description_message(match)

    return JsonResponse(slack_message)


@csrf_exempt
def actions(request: HttpRequest) -> HttpResponse:
    # print(request.POST)
    # if not is_slack_token_valid(request):
    #     return HttpResponseForbidden()
    payload_json = request.POST['payload']
    payload = json.loads(payload_json)

    # get user
    slack_user = get_or_create_slack_user(
        team=payload['team']['domain'],
        user_id=payload['user']['id'],
        username=payload['user']['name'])

    match = Match.objects.get(pk=payload['callback_id'])

    # join match
    success = join_match(match, slack_user.user)

    # update msg
    if success and is_match_full(match):
        slack_message = match_started_message(match)
        requests.post(url=payload['response_url'], json=slack_message)
    elif success:
        slack_message = match_description_message(match)
        requests.post(url=payload['response_url'], json=slack_message)

    return HttpResponse()
