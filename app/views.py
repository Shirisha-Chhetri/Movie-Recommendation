from django.shortcuts import render,redirect
from django.http import HttpResponse

from .ml import get_recommendation_for_movie

from .forms import MovieForm,ReviewForm, UploadForm
from .models import Movie,Review

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate,login
import math

from django.db import transaction
import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import MovieSerializer

# Create your views here.
def home(request):
    return HttpResponse("Home Page")

def number(request,id):
    return HttpResponse("Number " + str(id))

def template_test(request):
    return render(request,'index.html')

def get_movie_info(request,id):
    #request ma ahileko logged in user info huncha
    try:
        review_form = ReviewForm()
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                #commit=false means db ma objects bancha but save hudaina 
                # as extra info of user and movie dina baki vha
                review.movie_id = id
                review.user_id = request.user.id
                review.save()

        movie = Movie.objects.get(id = id)
        #-(minus)created_at menas decending order [0-4]means only 4 data
        reviews = Review.objects.filter(movie = movie).order_by('-created_at')[0:4]

        context = {
            'is_favourite' :False
        }

        #for recommendation
        movie_ids = get_recommendation_for_movie(id)
        recommend_movies = Movie.objects.filter(id__in = movie_ids)

        
        #pk = primary key
        if movie.favourite.filter(pk = request.user.pk).exists():
            context['is_favourite']= True

        return render(request,'movie.html',
        {'movie':movie,
        'context':context,
        'review_form':review_form,
        'reviews':reviews,
        'recommended_movies': recommend_movies
        })

    except Movie.DoesNotExist:
        return render(request,'404.html')


#for pagination also
def get_allmovie(request, page_number):
    #page_size = means number of data to be displayed in a single page
    page_size = 15
    
    if page_number < 1:
        page_number = 1
    
    movie_count = Movie.objects.count()

    last_page = math.ceil(movie_count / page_size)

    pagination = {
        'previous_page' : page_number -1,
        'current_page': page_number,
        'next_page': page_number + 1,
        'last_page' : last_page
    }

    movies = Movie.objects.all()[
        (page_number-1) * page_size : page_number*page_size]
    return render(request, 'movies.html',{
        'movies':movies,
        'pagination':pagination
        })

def post_movie(request):
    form = MovieForm()

    if request.method == "POST":
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()

            return redirect('/movie/')
    return render(request,'post_movie.html',{'form': form})

def signin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)

        if form.is_valid():
            user = authenticate(
                #cleaned_data save from sqlinjection attack
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            login(request,user)
            return redirect('/movie/page/1')
    return render(request,'signin.html',{'form':form})

def add_fav(request,id):
    movie = Movie.objects.get(id = id)
    movie.favourite.add(request.user)

    return redirect('/movies/{0}'.format(id))

def remove_fav(request,id):
    movie = Movie.objects.get(id = id)
    movie.favourite.remove(request.user)

    return redirect('/movies/{0}'.format(id))

def get_user_fav(request):
    movies =request.user.favourite.all()
    return render(request,'user_fav.html',{'movies':movies})

def upload_dataset(request):
    file_form = UploadForm()
    error_messages = {}

    if request.method == "POST":
        # file upload garna form and file successively
        file_form = UploadForm(request.POST, request.FILES)
        try:
            if file_form.is_valid():
                # pandas ko dataframe banaucha
                dataset = pd.read_csv(request.FILES['file'])
                new_movies_list =[]
                # budget chaina bhane 0 banucha
                # dataset['budget'] = dataset['budget'].fillna(0)

                # gives ACID property of db wg moview ra review ma dubai ma rakhna pare as Acid
                with transaction.atomic():

                    # movies ko oject banaucha
                    for index, row in dataset.iterrows():
                        movie = Movie(
                            title = row['title'],
                            budget = row['budget'],
                            genres = row['genres'],
                            keywords = row['keywords'],
                            overview = row['overview'],
                            tagline = row['tagline'],
                            cast = row['cast'],
                            director = row['director']
                        )
                        new_movies_list.append(movie)
                Movie.objects.bulk_create(new_movies_list)
                return redirect('/movie/page/1')

        except Exception as e:
            error_messages['error'] = e

    return render(request, 'upload_dataset.html',{'form' : file_form,
                                    'error_messages': error_messages})

class RetrieveMovieList(APIView):
    def get(self, request):
        movies = Movie.objects.all()[0:10]
        serializer = MovieSerializer(movies,many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)

class CreateMovie(APIView):
    def post(self,request):
        serializer = MovieSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get movie info ko previous data lai api ma send gareko i.e it is the same data as above
class GetMovieRecommendation(APIView):
    def get(self,request,id):
        movie_ids = get_recommendation_for_movie(id)
        recommend_movies = Movie.objects.filter(id__in = movie_ids)
        serializer = MovieSerializer(recommend_movies, many= True)
        return Response(serializer.data,status= status.HTTP_200_OK)