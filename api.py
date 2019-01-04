import os

import requests
import json

key = '152b8c4c817fcf8330f2e06fe7d6a009'


def search_movie(query):
    API = 'https://api.themoviedb.org/3/search/movie?api_key=152b8c4c817fcf8330f2e06fe7d6a009&language=en-US&page=1&include_adult=false'
    result = requests.get(API, params={
        'query': query,
        'page': 1,

    }, timeout=2)
    res = result.json()
    normal_result = {}
    t = 0
    try:
        for i in res['results']:
            id = i['id']
            title = i['title']
            normal_result[id] = title
            t = t + 1
            if t >= 4:
                break
    except Exception as e:
        return []
    return normal_result


def search_people(query):
    API = 'https://api.themoviedb.org/3/search/person?api_key=152b8c4c817fcf8330f2e06fe7d6a009&language=en-US&page=1&include_adult=false'
    result = requests.get(API, params={'query': query, 'page': 1, }, timeout=2)
    res = result.json()
    normal_result = {}
    try:
        if res["total_results"] is not 0:
            known_for = res['results'][0]['known_for']
            t = 0
            for i in known_for:
                id = i['id']
                title = i['title']
                normal_result[id] = title
                t = t + 1
                if t > 4:
                    break
    except Exception as e:
        return []
    return normal_result


def get_now_playing_movies():
    API = 'https://api.themoviedb.org/3/movie/now_playing?api_key=152b8c4c817fcf8330f2e06fe7d6a009&language=en-US&page=1'
    result = requests.get(API, params={
        'page': 1,

    }, timeout=2)
    res = result.json()
    if res['total_results'] is not None:
        normal_result = {}
        for i in res['results']:
            id = i['id']
            name = i['original_title']
            normal_result[id] = name
        return normal_result
    else:
        return []


def get_movie_information(id):
    API = 'https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=152b8c4c817fcf8330f2e06fe7d6a009&language=en-US'
    result = requests.get(API, params={}, timeout=2)
    res = result.json()
    movie_info_list = {}
    movie_info_list['genres'] = [i['name'] for i in res['genres']]
    movie_info_list['title'] = res['original_title']
    movie_info_list['release_date'] = res['release_date']
    movie_info_list['rating'] = res['vote_average']
    movie_info_list["vote_count"] = res["vote_count"]
    movie_info_list['overview'] = res['overview']
    return movie_info_list


def get_movie_review(id):
    API_review = 'https://api.themoviedb.org/3/movie/' + str(
        id) + '/reviews?api_key=152b8c4c817fcf8330f2e06fe7d6a009&language=en-US&page=1'
    result2 = requests.get(API_review, params={})
    fetch_movie_review = result2.json()

    if fetch_movie_review['total_results'] is 0:
        return "no review"
    else:
        return fetch_movie_review['results'][0]['content']


def get_similar_movie(id):
    API = 'https://api.themoviedb.org/3/movie/' + str(
        id) + '/similar?api_key=152b8c4c817fcf8330f2e06fe7d6a009&language=en-US&page=1'
    result = requests.get(API, params={}, timeout=2)
    res = result.json()
    normal_result = {}
    t = 0
    for i in res['results']:
        id = i['id']
        title = i['original_title']
        normal_result[id] = title
        t = t + 1
        if t > 5:
            break
    return normal_result


def get_movie_cast(id):
    API = 'https://api.themoviedb.org/3/movie/' + str(id) + '/credits?api_key=152b8c4c817fcf8330f2e06fe7d6a009'
    result = requests.get(API, params={}, timeout=2)
    res = result.json()
    normal_result = {}
    t = 0
    for i in res['cast']:
        name = i['name']
        character = i['character']
        normal_result[name] = character
        t = t + 1
        if t > 3:
            break

    normal_result['director'] = res['crew'][1]['name']
    return normal_result


if __name__ == '__main__':
    # print(get_now_playing_movies())
    # print(get_now_playing_movies().keys())
    #
    # a=get_now_playing_movies().keys()
    #
    # for i in a:
    #   info=get_movie_information(i)
    #   print(info['title'],info['genres'])

    print(search_movie('godfather'))
    print(search_movie("afsfafgedgfew"))
    print(search_people("Tom Cruise"))
    print(search_people("adasfdsfdsfgsdf"))
    print(get_similar_movie(236))
    print(get_movie_cast(238))
    print(get_movie_review(238))

    print(get_movie_review(335983))
