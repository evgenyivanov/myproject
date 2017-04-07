#  coding: utf-8
from django import forms


class ImageUploadForm(forms.Form):
    image = forms.FileField()

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField( widget=forms.PasswordInput)

class ChangePassword(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput, label = 'Новый пароль')
    password_repeat = forms.CharField(widget = forms.PasswordInput, label = 'Повторите пароль')
    def clean(self):
        from_data = self.cleaned_data
        if from_data['password'] != from_data['password_repeat']:
            self._errors['password'] = ['Пароли не совпадают']
            del from_data['password']
            return from_data
