from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model



class LoginForm(forms.Form):
    email = forms.CharField(required=True, label='Логин')
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput)
    next = forms.CharField(required=False, widget=forms.HiddenInput)


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, required=True, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username',  'email', 'avatar', 'password', 'password_confirm',
                  'first_name', 'additional', 'phone', 'gender')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'avatar', 'first_name',
                  'last_name', 'additional', 'phone', 'gender',)
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти пользователя')

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=3000, required=False, label='Комментарий',
                              widget=forms.Textarea(attrs={'name': 'body', 'rows': 5, 'cols': 21}))



class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)


    # def clean_password_confirm(self):
    #     password = self.cleaned_data.get("password")
    #     password_confirm = self.cleaned_data.get("password_confirm")
    #     if password and password_confirm and password != password_confirm:
    #         raise forms.ValidationError('Пароли не совпадают!')
    #     return password_confirm
    #
    # def clean_old_password(self):
    #     old_password = self.cleaned_data.get('old_password')
    #     if not self.instance.check_password(old_password):
    #         raise forms.ValidationError('Старый пароль неправильный!')
    #     return old_password
    #
    # def save(self, commit=True):
    #     user = self.instance
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
    #
    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']