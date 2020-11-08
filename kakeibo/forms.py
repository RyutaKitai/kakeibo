from django import forms
from .models import Kakeibo, Goals


class KakeiboForm(forms.ModelForm):
    class Meta:
        model = Kakeibo
        fields = ['date', 'category', 'money', 'memo']


class GoalsForm(forms.ModelForm):
    class Meta:
        model = Goals
        fields = ['mothly_goal', 'weekly_goal', "memo"]
