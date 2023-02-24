import json
import steam.webapi as steam_api
import pprint
import urllib.request
from howlongtobeatpy import HowLongToBeat

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


def get_game_info(game_id: str) -> dict:
    """
    Gets details for a steam game from the storefront api. Returns a json as a dict.
    :param game_id:
    :type: str
    :return: game_info
    :type: dict
    """
    with urllib.request.urlopen(fr"https://store.steampowered.com/api/appdetails?appids={game_id}") as url:
        game_info = json.load(url)
    # pprint.pprint(game_info)
    return game_info


def get_review_info(game_id: str) -> dict:
    """
    Gets review info from steam storefront api, removes review text and returns a dict.
    :param game_id:
    :type: str
    :return review_info:
    :type: dict
    """
    with urllib.request.urlopen(fr"https://store.steampowered.com/appreviews/{game_id}?json=1&language=all") as url:
        response = json.load(url)

    review_info = response["query_summary"]

    # pprint.pprint(review_info)
    return review_info


def review_ratio(review_dict):
    """
    Calculates ratio of positive reviews to negative reviews from a game, returns a float between 0 and 1.

    :param review_dict:
    :type: dict
    :return:
    :type: float
    """
    positive = review_dict["total_positive"]
    negative = review_dict["total_negative"]

    ratio = positive / (positive + negative)

    return ratio


def game_completion_time(game_name):
    """
    Uses howlongtobeatpy as an API to find completion time of a game.
    :param game_name:
    :return:
    """
    results = list(HowLongToBeat().search(game_name))

    if results is not None and len(results) > 0:
        best_element = max(results, key=lambda element: element.similarity)

    else:
        raise Exception("There is no matching How Long To Beat name.")

    try:
        time_to_finish = best_element.all_styles
    except:
        raise Exception(f"The game does not have a play time category. Game URL is {best_element.game_web_link}")

    time_to_finish = time_to_finish * 60  # convert to minutes to match steam library data

    return time_to_finish


def game_summary(game_id: str, completion_time: float, play_time: float):
    info = get_game_info(game_id)
    score = get_review_info(game_id)

    game_name = info[str(game_id)]["data"]["name"]

    genres = info[str(game_id)]["data"]["genres"]
    genre_list = [v["description"] for v in genres]

    review_score = review_ratio(score)

    summary = {
        "game_id": str(game_id),
        "name": game_name,
        "genres": genre_list,
        "review_score": review_score,  # TODO expand into T/F fields for each possible genre
        "completion_time": completion_time,
        "play_time": play_time,
        "completion_ratio": play_time / completion_time

    }

    return summary


if __name__ == "__main__":
    user_library = get_library(user_id)  # TODO iterate over and extrace game id and play time for further functions
    info = get_game_info(440)
    score = get_review_info(440)
    time_to_finish = game_completion_time("Elden Ring")

    summary = game_summary(440, time_to_finish, 11111)
    print("done")
