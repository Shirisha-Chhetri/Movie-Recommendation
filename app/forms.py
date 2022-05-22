from dataclasses import field
from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    #gives meta means extra information about views and models
    class Meta:
        model = Movie
        fields = ['title','budget','genres']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']


#csv file upload garne
class UploadForm(forms.Form):
    file = forms.FileField()

    # file upload garna milcha a file is input