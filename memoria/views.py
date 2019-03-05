# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import *

def signup(request):
	if request.user.is_authenticated:
		return redirect('/profile')
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			if form.is_data_valid():
				user = form.save()
				auth.login(request, user)
				return redirect('/profile')
			else:
				return redirect('.')
		else:
			return redirect('.')
	else:
		form = SignupForm()
		args = {'form': form}
		return render(request, 'registration/signup.html', args)

# def login():
# 	pass

def base_view(request, template_name='memoria/base_view.html'):
	if request.user.is_authenticated:
		return redirect('/profile')
	return render(request, template_name)

@login_required(login_url="/")
def user_details(request, template_name='memoria/profile.html'):
	user = request.user
	return render(request, template_name, {'user': user})

@login_required(login_url="/")
def book_list(request, template_name='memoria/books/books_list.html'):
	books = Book.objects.filter(author=request.user.pk).order_by('published_date')
	return render(request, template_name, {'books':books})

@login_required(login_url="/")
def book_view(request, pk, template_name='memoria/books/book_view.html'):
	book = get_object_or_404(Book, pk=pk)
	return render(request, template_name, {'book':book})

@login_required(login_url="/")
def book_create(request, template_name='memoria/books/book_create.html'):
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			book = form.save(commit=False)
			book.author = request.user
			book.published_date = timezone.now()
			book.save()
			return redirect('/books')
		else:
			return redirect('.')
	else:
		form = BookForm()
		args = {'form': form}
		return render(request, template_name, args)

@login_required(login_url="/")
def book_edit(request, pk, template_name='memoria/books/book_edit.html'):
	book = get_object_or_404(Book, pk=pk)
	if request.method == "POST":
		book.name = request.POST.get("name")
		book.comment = request.POST.get("comment")
		book.save()
		return redirect('/books')
	else:
		return render(request, template_name, {'book':book})

@login_required(login_url="/")
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('/books')

@login_required(login_url="/")
def film_list(request, template_name='memoria/films/films_list.html'):
	films = Film.objects.filter(author=request.user.pk).order_by('published_date')
	return render(request, template_name, {'films':films})

@login_required(login_url="/")
def film_view(request, pk, template_name='memoria/films/film_view.html'):
	film = get_object_or_404(Film, pk=pk)
	return render(request, template_name, {'film':film})

@login_required(login_url="/")
def film_create(request, template_name='memoria/films/film_create.html'):
	if request.method == "POST":
		form = FilmForm(request.POST)
		if form.is_valid():
			film = form.save(commit=False)
			film.author = request.user
			film.published_date = timezone.now()
			film.save()
			return redirect('/films')
		else:
			return redirect('.')
	else:
		form = FilmForm()
		args = {'form': form}
		return render(request, template_name, args)

@login_required(login_url="/")
def film_edit(request, pk, template_name='memoria/films/film_edit.html'):
	film = get_object_or_404(Film, pk=pk)
	if request.method == "POST":
		film.name = request.POST.get("name")
		film.comment = request.POST.get("comment")
		film.save()
		return redirect('/films')
	else:
		return render(request, template_name, {'film':film})

@login_required(login_url="/")
def film_delete(request, pk):
	film = get_object_or_404(Film, pk=pk)
	film.delete()
	return redirect('/films')

@login_required(login_url="/")
def tvseries_list(request, template_name='memoria/tvseries/tvseries_list.html'):
	tvseries = TVSeries.objects.filter(author=request.user.pk).order_by('published_date')
	return render(request, template_name, {'tvlist':tvseries})

@login_required(login_url="/")
def tvseries_view(request, pk, template_name='memoria/tvseries/tvseries_view.html'):
	tvseries = get_object_or_404(TVSeries, pk=pk)
	return render(request, template_name, {'tvseries':tvseries})

@login_required(login_url="/")
def tvseries_create(request, template_name='memoria/tvseries/tvseries_create.html'):
	if request.method == "POST":
		form = TVSeriesForm(request.POST)
		if form.is_valid():
			tvseries = form.save(commit=False)
			tvseries.author = request.user
			tvseries.published_date = timezone.now()
			tvseries.save()
			return redirect('/tvseries')
		else:
			return redirect('.')
	else:
		form = TVSeriesForm()
		args = {'form': form}
		return render(request, template_name, args)

@login_required(login_url="/")
def tvseries_edit(request, pk, template_name='memoria/tvseries/tvseries_edit.html'):
	tvseries = get_object_or_404(TVSeries, pk=pk)
	if request.method == "POST":
		tvseries.name = request.POST.get("name")
		tvseries.comment = request.POST.get("comment")
		tvseries.save()
		return redirect('/tvseries')
	else:
		return render(request, template_name, {'tvseries':tvseries})

@login_required(login_url="/")
def tvseries_delete(request, pk):
	tvseries = get_object_or_404(TVSeries, pk=pk)
	tvseries.delete()
	return redirect('/tvseries')
