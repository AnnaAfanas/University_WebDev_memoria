from django import forms
import re
from django.contrib.auth.models import User
from .models import *

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ('name', 'comment')

class FilmForm(forms.ModelForm):
	class Meta:
		model = Film
		fields = ('name', 'comment')

class TVSeriesForm(forms.ModelForm):
	class Meta:
		model = TVSeries
		fields = ('name', 'comment')


class LoginForm(forms.ModelForm):
	username = forms.CharField(label='Логин',
							   max_length=10,
							   error_messages={'required': 'Укажите логин'})
	password = forms.CharField(label='Пароль',
							   widget=forms.PasswordInput(),
							   error_messages={'required':'Укажите пароль'})
	class Meta:
		model = User
		fields = ('username', 'password')

	def is_data_valid(self):
		if re.match('^[a-zA-Z0-9а-яА-Я_]+$', self.cleaned_data.get('username')) == False:
			return False
		if len(self.cleaned_data.get('username')) < 4 and len(self.cleaned_data.get('username')) > 10:
			return False
		return True

class SignupForm(forms.ModelForm):
	username = forms.CharField(label='Логин',
							   max_length=10,
							   error_messages={'required': 'Укажите логин'})
	password = forms.CharField(label='Пароль',
							   widget=forms.PasswordInput(),
							   error_messages={'required': 'Укажите пароль'})
	password_confirmation = forms.CharField(label='Подтверждение пароля',
											widget=forms.PasswordInput(),
											error_messages={'required': 'Подтвердите пароль'})
	class Meta:
		model = User
		fields = ('username', 'password', 'password_confirmation')

	def is_data_valid(self):
		if re.match('^[a-zA-Z0-9_]+$', self.cleaned_data['username']) == False:
			return False
		if len(self.cleaned_data['username']) < 4 or len(self.cleaned_data['username']) > 10:
			return False
		if len(self.cleaned_data['password'])< 6:
			return False
		if self.cleaned_data['password'] != self.cleaned_data['password_confirmation']:
			return False
		return True
