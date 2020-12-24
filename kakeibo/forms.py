from django import forms
from .models import Kakeibo, Goals, Category
from .fileds import SimpleCaptchaField
from django.contrib.auth import forms as auth_forms


class LoginForm(auth_forms.AuthenticationForm):
    '''ログインフォーム'''

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


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
