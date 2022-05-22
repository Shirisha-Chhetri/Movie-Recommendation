"""django_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('',views.home),
    path('number/<int:id>',views.number),
    path('index/',views.template_test),
    path('movies/<int:id>',views.get_movie_info),
    path('movie/page/<int:page_number>',views.get_allmovie),
    path('post_movie/',views.post_movie),
    path('admin/', admin.site.urls),
    path('signin/',views.signin, name="User Signin"),

   # pathname is of movie.html
    path('add_to_fav/<int:id>',views.add_fav,name="Add to favourite"),
    path('remove_from_fav/<int:id>',views.remove_fav,name="Remove from favourite"),
    path('user_fav/',views.get_user_fav),

    path('upload_dataset/',views.upload_dataset,name = "Upload dataset"),

    path('api/movies', views.RetrieveMovieList.as_view(),name="get_movies_api"),

    path('api/recommended_movie/<int:id>',views.GetMovieRecommendation.as_view(),
    name = "get_movies_recommendation_api"),
    
    path('api/add_movie',views.CreateMovie.as_view(),name = 'add_movie'),
]