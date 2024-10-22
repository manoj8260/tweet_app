from django import forms
from .models import * 
class UserModel(forms.ModelForm):
    class Meta:
        model = User
        fields =['first_name','last_name','email','username','password']
        help_texts={'username':' '}

class ProfileModel(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=['username']

class TweetModel(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude=['username','like']

       
