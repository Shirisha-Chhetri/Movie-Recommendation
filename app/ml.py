#for recommendation

import pandas as pd
from sklearn.feature_extraction.text  import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Movie

def combined_features(row):
    return row['genres']+" " + row['keywords']+" "
    + row['cast']+ " "+ row['director']+ " " +row['overview'] 

def get_id_from_inside(df,index):
    return df[df.index == index]["id"].values[0]

def get_index_from_id(df,id):
    return df[df.id == id].index.values[0]

def get_recommendation_for_movie(movie_id):
    df = pd.DataFrame(list(Movie.objects.all().values()))
    features = ['keywords','cast','overview','genres','director']
    for feature in features:
        df[feature] = df[feature].fillna('')

    df['combined_features'] = df.apply(combined_features,axis =1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)
    id = get_index_from_id(df,movie_id)
    similar_movies = list(enumerate(cosine_sim[id]))

    sorted_similar_movies = sorted(
        similar_movies, key = lambda x: x[1], reverse=True)
         
    i =0
    movie_ids =[]
    for movie in sorted_similar_movies:
        i = i+1
        movie_ids.append(get_id_from_inside(df,movie[0]))

        if i> 15:
            break
    return movie_ids

