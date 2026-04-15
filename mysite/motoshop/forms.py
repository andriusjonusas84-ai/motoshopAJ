from django.contrib.auth.forms import UserCreationForm
from .models import  CustomUser,ProductReview
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['content']

class ProductFilterForm(forms.Form):
    title = forms.CharField()