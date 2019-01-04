
This project uses RASA CORE and RASA NLU to establish chabot which can answer questions about movies. 
RASA is a very useful tool, and we can use it to construct more robust chatbot more quickly compared with pure NLP technology, such as seq2seq or attention model. So in the end, we used RASA NLU to fulfill basic intention recognition and entity extraction, and we used RASA CORE to fulfill dialogue management. And finally we deploy the whole framework to social media software like Wechat to realize more real and convenient human-machine interaction. 

We Choose movie information query as main QA domain of our chatbot. Unlike some software like Doubai or IMDb, the user just need to input whole sentences to get information they want.

## 1.design and recognition of intentions and entity about movie information query  
We define 10 kind frequent intention as follow
- greet   - thank
  - ask_now_playing_movies(ask bot what movie is on in the cinema)
  - ask_movie_information(ask bot type and overview of the movie )
  - ask_movie_rating(ask bot the rating of the movie)
  - ask_movie_stars(ask bot cast of the movie)
  - ask_star_movies(ask famous movie of the star)
  - dislike_movie(express dislike to the movie)
  - like_movie(express great interest to the movie)
  - ask_related_recommendation(ask related or similar other movies with the movie)

And we design concrete question data in nlu.json, the pattern is showed as followed
 {  "text":"I want to ask information about Interstellar",
    "intent":"ask_movie_information",
"entities":[  { "start":32, "end": 44,  "value":"Interstellar",  "entity":"movie"}]},

And we also define pipelines for RASA NLU, it’s configuration of libraries, for example, we can use ner_synonyms to better recognize synonyms in difference sentences of same intention.  

 Now, we can use train RASA NLU with those JSON data using libraries in pipelines, and get temporary results of intention recognition and entity extraction. 


## 2.design of answers with querying API 
Based on known questions with their entity and intention, we need to design corresponding problems. In this project, I use TMDbs to query information.  
 
We can search information about films about stars in this API, we can use python to request JSON data in this API and clean data to return desired results.

In file domain.yml, we list all intents,entities actions which will be used latter, we have to noted there that Action is concrete answers to different kinds of specific question. We define all Actions in action.py. Those functions in this files encapsulate returned API data, and finally return whole textual sentences. For example, the ActionMovieRating as follow defines answer to ask_movie_rating, and those action also can keep track of entities in context, for example, if I ask “I want to know the rating of this movie”, the Action will fetch value in “movie” slot which is identified and stored in previous Q&A process.

Now, we need define stories to simulate finite state machine, the RASA NLU need to know what real conversations are and train itself with data. In the file stories.md, we write many possible conversations which contain different intents of question and corresponding answers. For example, The case of lastest movies3, the user may ask what movie is on now, then the bot lists all hot movies in the cinema, and then the user may ask one specific movie among them, and the robot will answer concrete details. In the end, the user may show great interest about this movie, the bot can thus actively show similar movies for the user. Compared with traditional FSM, this technology can deal with more complex case, and large-scale data.


## 3.Integrating of whole framework and testing 

In the run.py, we combine all the work above. We train RASA NLU to get NLU Interpreter, and We use RASA NLU’s agent to train stories with using NLU interpreter. We also define scientific training policies in the file policies.yml.

In the end, we test it and get good outcome. For example, the chatbot can accurately offer answers about movie’s information and rating.
