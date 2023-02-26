
from django.urls import path
from .views import users_list, user_profile, follow_unfollow, follow_request_requested, accept, direct, my_directs_view, followerings, register, user_login, changepass, loggedout, Edit_Profile
from django.views.generic import TemplateView

app_name = 'account'

urlpatterns = [
    path('users_list/', users_list, name='users_list'),
    path('users_profile/<int:id>/', user_profile, name='user_profile'),
    path('editprofile/', Edit_Profile, name='editprofile'),
    path('changepass/', changepass, name='changepassword'),
    path('login/', user_login, name='login'),
    path('logout/', loggedout, name='logout'),
    path('register/', register, name='register'),
    path('follow_unfollow/', follow_unfollow, name='follow_unfollow'),
    path('follow_request_requested/', follow_request_requested, name='follow_request_requested'),
    path('accept/<int:id>/<str:identifier>/', accept, name='accept'),
    path('direct/<int:id>/', direct, name='direct'),
    path('mydirects/', my_directs_view, name='my_directs'),
    path('followerings/<int:id>/<str:identifier>/', followerings, name='followerings'),
]
