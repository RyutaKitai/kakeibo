from django import forms 
from .models import Kakeibo

class KakeiboForm(forms.ModelForm):
    class Meta:
        """
        新規データ登録画面用のフォーム定義
        """
        model = Kakeibo
        fields = ['date', 'category', 'money', 'memo']
