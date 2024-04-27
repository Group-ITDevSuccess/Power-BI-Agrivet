from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate-uid/', views.generate_uid, name='generate_uid'),
    path('get-all-hebdo/', views.get_all_hebdo, name='get_all_hebdo'),
    path('create-or-update-hebdo/', views.create_or_update_hebdo, name='create_or_update_hebdo'),
    path('delete-hebdo-by-uid/', views.delete_hebdo_by_uid, name='delete_hebdo_by_uid'),
]