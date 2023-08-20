from django.urls import path
from . import views
from .views import UploadReplay, Toglelike, TogleBookmark, Profile, Search

urlpatterns = [
    path('', views.home, name='login'),
    path('main/', views.get, name='main'),
    path('home/upload', views.post, name='upload'),
    # path('main/profile', views.profile, name='profile'),
    path('main/profile', Profile.as_view(), name='profile'),
    path('main/replyadd', UploadReplay.as_view(), name='replyadd'),
    path('main/like', Toglelike.as_view(), name='like'),
    path('main/bookmark', TogleBookmark.as_view(), name='bookmark'),
    path('main/search', Search.as_view(), name='search')
]