from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib import auth
from memoria import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.base_view, name='base_view'), 
    url(r'^login/$', auth_views.LoginView.as_view(),name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('base_view')), name='logout'),

    url(r'^profile/$', views.user_details, name='profile'),

    url(r'^books/$', views.book_list, name='book_list'),
    url(r'^films/$', views.film_list, name='film_list'),
    url(r'^tvseries/$', views.tvseries_list, name='tvseries_list'),

    url(r'^books/new$', views.book_create, name='book_create'),
    url(r'^books/(?P<pk>\d+)$', views.book_view, name='book_view'),
    url(r'^books/(?P<pk>\d+)/edit$', views.book_edit, name='book_edit'),
    url(r'^books/(?P<pk>\d+)/delete$', views.book_delete, name='book_delete'),

    url(r'^films/new$', views.film_create, name='film_create'),
    url(r'^films/(?P<pk>\d+)$', views.film_view, name='film_view'),
    url(r'^films/(?P<pk>\d+)/edit$', views.film_edit, name='film_edit'),
    url(r'^films/(?P<pk>\d+)/delete$', views.film_delete, name='film_delete'),

    url(r'^tvseries/new$', views.tvseries_create, name='tvseries_create'),
    url(r'^tvseries/(?P<pk>\d+)$', views.tvseries_view, name='tvseries_view'),
    url(r'^tvseries/(?P<pk>\d+)/edit$', views.tvseries_edit, name='tvseries_edit'),
    url(r'^tvseries/(?P<pk>\d+)/delete$', views.tvseries_delete, name='tvseries_delete'),
]
