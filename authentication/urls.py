
from django.urls import path,include
from .views import *

from dj_rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', AccountUserViewset)


urlpatterns = [
<<<<<<< HEAD

    path('', include('djoser.urls')),
=======
    path('', include(router.urls)),

   # path('', include('djoser.urls')),
>>>>>>> 46ad1d0bf4569949ca9066f6e18705cc64c8a472
    path('', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.social.urls')),

    path('promote/', PromoteToVoteAdminView.as_view(), name='promote_to_vote_admin'),

    path('logout/', LogoutAPIView.as_view(), name="logout"),

<<<<<<< HEAD
    path('activate/<uid>/<token>/', activate, name='activate'),


=======
    path('user-me/update/', CustomUserViewset.as_view(), name='patch_user'),
    path('users/activation/<str:email>/<str:code>/', UserActivationView.as_view()),
    
>>>>>>> 46ad1d0bf4569949ca9066f6e18705cc64c8a472
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
