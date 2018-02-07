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
    token = request.POST.get('token')
    if token is None or not is_slack_token_valid(token):
        return HttpResponseForbidden()

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
    payload_json = request.POST.get('payload', '')
    payload = json.loads(payload_json)
    token = payload.get('token')

    if token is None or not is_slack_token_valid(token):
        return HttpResponseForbidden()

    # get user
    slack_user = get_or_create_slack_user(
        team=payload['team']['domain'],
        user_id=payload['user']['id'],
        username=payload['user']['name'])

    match = Match.objects.get(pk=payload['callback_id'])

    # join match
    success, msg = join_match(match, slack_user.user)

    # update msg
    if not success:
        # todo: we can send separate msg to chanell in case of errors
        # return empty response
        return HttpResponse()
    if success and is_match_full(match):
        slack_message = match_started_message(match)
    elif success:
        slack_message = match_description_message(match)

    return JsonResponse(data=slack_message)
