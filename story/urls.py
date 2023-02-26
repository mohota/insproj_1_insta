
from django.urls import path
from .views import add_story


app_name = 'story'

urlpatterns = [
    path('add_story', add_story, name='add_story'),
   
]
