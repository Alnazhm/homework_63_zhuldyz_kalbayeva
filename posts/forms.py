from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from posts.models import Post


class PostForm(forms.ModelForm):
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'name': 'body', 'rows': 5, 'cols': 21})
    )

    class Meta:
        model = Post
        fields = ('image', 'description',)
        widgets = {
            'description': forms.Textarea(attrs={'cols': 21, 'rows': 5}),
        }
