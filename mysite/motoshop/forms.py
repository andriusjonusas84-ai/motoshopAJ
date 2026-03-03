from tokenize import Comment

from django.contrib.auth.forms import UserCreationForm
from .models import  CustomUser,Order,Product,OrderLine,ProductCategory,ProductReview
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['content']