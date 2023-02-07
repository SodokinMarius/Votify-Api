
from django.urls import path,include 
from .views import *

from dj_rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)

urlpatterns = [
    
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.social.urls')),
    #path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('users/{id}/subscribe/', UserViewSet.as_view({'post': 'subscribe'}), name='user-subscribe'),

    path('logout/', LogoutAPIView.as_view(), name="logout"),
    
    #--------------------------------#
    #            GOOBLE              #
    #--------------------------------#
    path('google/', GoogleLogin.as_view(), name='google_login'),

   
    #--------------------------------#
    #          FACEBOOK              #
    #--------------------------------#
    path('facebook/', FacebookLogin.as_view(), name='facebook_login'),


    
 
    #------------------------------------------#
    #          ALL SOCIAL ACCOUNT              #
    #------------------------------------------#

    path('socialaccounts/',SocialAccountListView.as_view(),name='social_account_list'),
    path('socialaccounts/<int:pk>/disconnect/',SocialAccountDisconnectView.as_view(),name='social_account_disconnect' )


]
