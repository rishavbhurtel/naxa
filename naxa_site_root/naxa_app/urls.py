from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_user, name='logout'),
    path('list', views.list_users, name='list'),
    path('line', views.geo_json, name='geo_json'),
    path('nearby', views.nearby, name='nearby'),
]
