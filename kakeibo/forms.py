from django import forms
from .models import Kakeibo, Goals, Category
from .fileds import SimpleCaptchaField


class KakeiboForm(forms.ModelForm):
    class Meta:
        model = Kakeibo
        fields = ['date', 'category', 'money', 'memo']


class GoalsForm(forms.ModelForm):
    class Meta:
        model = Goals
        fields = ['mothly_goal', 'weekly_goal', 'memo']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
