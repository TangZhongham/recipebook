from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Recipe, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 
                 'cooking_time', 'cuisine_type', 'dietary_restrictions', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 
        