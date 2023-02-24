import json
import steam.webapi as steam_api
import pprint
import urllib.request

with open(r"apikey.json") as f:
    api_userid = json.load(f)

api_key = api_userid["steam_api_key"]
user_id = api_userid["user_id"]

api = steam_api.WebAPI(key=api_key)


def get_library(user_id: str, api=api) -> list:
    """
    Query's steams web api and returns a list of all games tied to a user id as a list of dictionaries.

    :param user_id: user id from s://steamcommunity.com/profiles/{USER_ID}/
    :type: str
    :param api: steamapi object
    :return: list of all game dictionaries
    :type: list
    """
    response = api.IPlayerService.GetOwnedGames(steamid=user_id,
                                                include_appinfo=True,
                                                include_played_free_games=True,
                                                appids_filter=False,
                                                include_free_sub=True,
                                                language='english',
                                                include_extended_appinfo=False)

    # pprint.pprint(response)
    user_library = response["response"]["games"]
    return user_library


def get_game_info(game_id):
    """

    :param game_id:
    :return:
    """
    with urllib.request.urlopen(fr"https://store.steampowered.com/api/appdetails?appids={game_id}") as url:
        game_info = json.load(url)
    # pprint.pprint(game_info)
    return game_info


def get_review_info(game_id):

    with urllib.request.urlopen(fr"https://store.steampowered.com/appreviews/{game_id}?json=1&language=all") as url:
        response = json.load(url)

    review_info = response["query_summary"]


    pprint.pprint(review_info)
    return review_info


def review_ratio(review_dict):
    positive = review_dict["total_positive"]
    negative = review_dict["total_negative"]

    ratio = positive / (positive + negative)

    return ratio


if __name__ == "__main__":
    user_library = get_library(user_id)
    info = get_game_info(440)
    score = get_review_info(440)

    print("done")
