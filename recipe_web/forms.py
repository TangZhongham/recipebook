from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Recipe, Comment
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model  


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
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
        
        
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput, 
        label="New Password", 
        min_length=8,  # 设置最小长度要求
        max_length=128,  # 设置最大长度要求
        help_text="Your password must be at least 8 characters long."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        if new_password and len(new_password.strip()) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        return cleaned_data