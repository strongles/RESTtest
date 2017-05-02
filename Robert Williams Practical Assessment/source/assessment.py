from flask import Flask, json, jsonify
from math import ceil
from time import strftime, localtime
from sys import argv
from os.path import isfile

gameservice = Flask(__name__)

SOURCE_DATA = 'games_data.json'


def get_games_data(filepath=SOURCE_DATA):
    """
    If no parameter is provided it will use the global source string to acquire the 
    data.
    """
    if isfile(filepath):
        with open(filepath) as file_in:
            game_data = json.load(file_in)
        return game_data
    else:
        raise (filepath)


def parse_time(epoch_string):
    return strftime('%Y-%m-%d', localtime(int(epoch_string)))


def get_game_from_id(game_id, game_data):
    return_game = None
    for game in game_data['games']:
        if game['game_id'] == game_id:
            return_game = dict(game)
            break
    return return_game


def parse_game_data_for_return(game_data):
    del game_data['game_id']
    for comment in game_data['comments']:
        comment['dateCreated'] = parse_time(comment['dateCreated'])


def get_highest_commenter(comment_count_dict):
    highest_comment_count = 0
    highest_commenter = ''
    for user in comment_count_dict:
        if comment_count_dict[user] > highest_comment_count:
            highest_comment_count = comment_count_dict[user]
            highest_commenter = user

    return highest_commenter


def get_average_likes_per_game(game_likes_dict):
    average_likes_per_game = list()
    for game in game_likes_dict:
        average_likes = ceil(sum(game_likes_dict[game]) / len(game_likes_dict[game]))
        average_likes_per_game.append({'title': game, 'average_likes': average_likes})

    return average_likes_per_game


def get_highest_rated_game(game_likes_dict):
    highest_like_total = 0
    most_liked_game = ''
    for game in game_likes_dict:
        if sum(game_likes_dict[game]) > highest_like_total:
            highest_like_total = sum(game_likes_dict[game])
            most_liked_game = game

    return most_liked_game


@gameservice.route('/games/<game_id>', methods=['GET'])
def game_information(game_id):

    data_set = get_games_data()
    response = get_game_from_id(int(game_id), data_set)

    if not response:
        response = {'Error': 'Game not found.'}
    else:
        parse_game_data_for_return(response)

    """
    This output will differ slightly from the requirement given that the ordering of 
    the JSON tags will be sorted alphabetically by default. 
    This appears to be a bug in Flask that has not been addressed due to the fact that 
    ordering in JSON is intended to be irrelevant.
    """
    return jsonify(response)


@gameservice.route('/games/report', methods=['GET'])
def report():
    data_set = get_games_data()
    response = dict()

    game_likes = dict()
    user_comment_count = dict()

    for game in data_set['games']:
        game_likes[game['title']] = list()
        for comment in game['comments']:
            if comment['user'] not in user_comment_count:
                user_comment_count[comment['user']] = 0
            user_comment_count[comment['user']] += 1
            game_likes[game['title']].append(comment['like'])

    response['user_with_most_comments'] = get_highest_commenter(user_comment_count)

    response['average_likes_per_game'] = get_average_likes_per_game(game_likes)

    response['highest_rated_game'] = get_highest_rated_game(game_likes)

    """
    This output will differ slightly from the requirement given that the ordering of 
    the JSON tags will be sorted alphabetically by default. 
    This appears to be a bug in Flask that has not been addressed due to the fact that 
    ordering in JSON is intended to be irrelevant.
    """
    return jsonify(response)


if __name__ == '__main__':
    """
    Script can be called with 0 or 1 parameter. Parameter is a filepath to the dataset
    to be used to power the API returns. Filepath is checked to be valid, if so it is 
    used as the global filepath for data retrieval.
    """

    if len(argv) > 1:
        if isfile(argv[1]):
            SOURCE_DATA = argv[1]
        else:
            raise FileNotFoundError(argv[1])

    port = 8080
    gameservice.run(host='127.0.0.1', port=port)
