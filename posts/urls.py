
from django.urls import path
from .views import add_post, post_detail

app_name = 'posts'

urlpatterns = [
    path('add/', add_post, name='add_post'),
    path('detail/<int:id>/', post_detail, name='post_detail'),
    
]
