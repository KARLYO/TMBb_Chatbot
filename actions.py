# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action

logger = logging.getLogger(__name__)


from rasa_core.events import SlotSet
from api import search_people,search_movie,get_movie_cast,get_similar_movie,get_movie_information,get_now_playing_movies


class ActionNowPlayingMovie(Action):
   def name(self):
       return "action_now_playing_movies"

   def run(self, dispatcher, tracker, domain):

       now=get_now_playing_movies()
       values=list(now.values())

       all_now="\n".join(values)
       response="Ok,those movies are on now:\n{}\nI hope you can enjoy them!".format(all_now)
       dispatcher.utter_message(response)
       return []



class ActionMovieInfo(Action):
    def name(self):
        return"action_movie_information"
    def run(self, dispatcher, tracker, domain):
        formal_name=''
        movie=tracker.get_slot("movie")
        print(movie)
        movie_2=search_movie(movie)
        if(len(movie_2) is 0):
          dispatcher.utter_message("sorry, we can't find the movie you want")
        else:
            id=list(search_movie(movie).keys())[0]
            formal_name=list(search_movie(movie).values())[0]
            overview=get_movie_information(id)["overview"]
            type=(" , ").join(get_movie_information(id)['genres'])
            response='Ok,{} is {} movie, and here is overview : {}'.format(movie,type,overview)
            dispatcher.utter_message(response)
        return []



class ActionMovieRating(Action):
    def name(self):
        return"action_movie_rating"

    def run(self, dispatcher, tracker, domain):
        formal_name = ''
        movie = tracker.get_slot("movie")
        print(movie)
        movie_2 = search_movie(movie)
        if (len(movie_2) is 0):
            dispatcher.utter_message("sorry, we can't find the movie you want")
        else:
            id = list(search_movie(movie).keys())[0]
            formal_name=list(search_movie(movie).values())[0]
            rating = get_movie_information(id)['rating']
            count= get_movie_information(id)['vote_count']
            response = 'the rating of {} is : {} , based on {} vote'.format(formal_name,rating,count)
            dispatcher.utter_message(response)
        return []

class ActionMoviesStars(Action):
    def name(self):
        return "action_movie_stars"
    def run(self, dispatcher, tracker, domain):
        formal_name=''
        movie=tracker.get_slot("star")
        print(movie)
        movie_2 = search_movie(movie)
        if (len(movie_2) is 0):
            dispatcher.utter_message("sorry, we don't find the movie you want")
        else:

            id = list(search_movie(movie).keys())[0]
            formal_name = list(search_movie(movie).values())[0]
            cast = get_movie_cast(id)
            long = ''
            for key, value in cast.items():
                if key is not "director":
                    cast_individual = '{} plays the role of {} \n'.format(key, value)
                    long = long + cast_individual

            response = "this is {}'s film, and here is cast: \n{} ".format(cast["director"], long)
            dispatcher.utter_message(response)
        return []

class ActionStarMovies(Action):
        def name(self):
            return "action_star_movies"

        def run(self, dispatcher, tracker, domain):
            values = []
            star = tracker.get_slot("star")
            movie_2 = search_people(star)
            if (len(movie_2) is 0):
                dispatcher.utter_message("sorry, we can't find the star you want ")
            else:
              keys=list(movie_2.keys())
              values=list(movie_2.values())

              Representive=",".join(values)
              response="here are {}'s famous movies:\n{}\nyou can ask me information about those movies".format(star,Representive)
              dispatcher.utter_message(response)
            return []

class ActionRecommendSimilarMovie(Action):
        def name(self):
            return "action_recommend_similar_movies"

        def run(self, dispatcher, tracker, domain):
            values=[]
            movie = tracker.get_slot("movie")
            movie_2 = search_movie(movie)
            if (len(movie_2) is 0):
                dispatcher.utter_message("sorry, we don't know what this film is ")
            else:
                id=search_movie(list(search_movie(movie).keys())[0])

                values = list(get_similar_movie(id).values())

                similar = "\n".join(values)
                response = "Ok, I find some movies like {} for you:\n{}\nI hope you will also enjoy those films".format(movie,similar)
                dispatcher.utter_message(response)
            return[]


class RecommendOtherMovies(Action):
    def name(self):
        return"action_recommend_other_movies"

    def run(self, dispatcher, tracker, domain):
        movies=[]
        movie=tracker.get_slot("movie")
        movies=tracker.get_slot("movies")

        if(len(movies) is 0):
            dispatcher.utter_message("I am sorry for hearing that, you can choose other films you like")
        else:
            movies2=[]
            for i in movies:
                if i is not movie:
                    movies2.append(i)
            res="\n".format(movies2)
            response="OK, I guess you may like those other films, I recommend those films for you:\n{}".format(res)
            dispatcher.utter_message(response)
            movies=movies2
        return[]