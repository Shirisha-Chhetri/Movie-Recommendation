from turtle import title
from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
from .models import Movie

class MovieTestCase(TestCase):
    def setUp(self):
        movie = Movie.objects.create(title = "Batman", budget="100000")

        user1 = User.objects.create_user(username = "Shally",
                                        email = "sahlly@gmail.com",
                                        password = 'shally123')

        user2 = User.objects.create_user(username = "Justin",
                                        email = "justin@gmail.com",
                                        password = 'justin123')
                                    
        movie.favourite.add(user1)
        movie.favourite.add(user2)

    def test_movie_name(self):

        #check for validation if I make Batman b small then it will say that the test is failed
        batman = Movie.objects.get(title="Batman")
        self.assertEqual(batman.title,"Batman")

    def test_budget_in_yen(self):
        #1230000 is the expected value in yen if I make 123 to 121 in models then it cause error
        batman = Movie.objects.get(title="Batman")
        self.assertEqual(batman.get_budget_in_yen(),12300000)

    def get_movie_users(self):
        batman = Movie.objects.get(title = "Batman")
        self.assertEqual(batman.favourite.count(),2)


