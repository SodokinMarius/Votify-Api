
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

    path('promote/', PromoteToVoteAdminView.as_view(), name='promote_to_vote_admin'),

    path('logout/', LogoutAPIView.as_view(), name="logout"),

    path('activate/<uid>/<token>/', activate, name='activate'),


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
