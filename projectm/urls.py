"""projectm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from apps.projectmAPI.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/v1/users/', UsersListView.as_view()),
    path('api/v1/users/exists/', IsUserExistsView.as_view()),
    #path('api/v1/users/add', UserAddView.as_view()),
    path('api/v1/users/me/', UserSelfInfoView.as_view()),
    path('api/v1/users/<int:uid>/', UserInfoView.as_view()),
    path('api/v1/users/<int:uid>/clubs/', UserClubsView.as_view()),
    path('api/v1/users/<int:uid>/clubs/<int:cid>/', UserInClubStatView.as_view()),
    path('api/v1/users/<int:uid>/clubs/<int:cid>/games/', UserClubGamesView.as_view()),
    path('api/v1/clubs/', ClubsListView.as_view()),
    path('api/v1/clubs/create/', ClubAddView.as_view()),
    path('api/v1/clubs/<int:cid>/adduser/', AddUserToClubView.as_view()),
    #path('api/v1/clubs/<int:cid>/join/'),
    path('api/v1/clubs/<int:cid>/', ClubInfoView.as_view()),
    path('api/v1/clubs/<int:cid>/users/', ClubUsersListView.as_view()),
    path('api/v1/clubs/<int:cid>/users/scoreboard/', ClubUsersScoreboardListView.as_view()),
    path('api/v1/clubs/<int:cid>/games/', ClubGamesView.as_view()),
    path('api/v1/games/', GamesListView.as_view()),
    path('api/v1/games/<int:gid>/', GameStatView.as_view()),
    path('api/v1/games/add/', GameAddView.as_view()),
    path('admin/', admin.site.urls),
    path(r'api/v1/auth/', include('djoser.urls')),
    re_path('^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
