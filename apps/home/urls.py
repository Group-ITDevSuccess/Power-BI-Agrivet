from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('get-all-hebdo/', views.get_all_hebdo, name='get_all_hebdo'),
]