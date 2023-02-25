
from django.urls import path,include
from .views import *

from dj_rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', AccountUserViewset)


urlpatterns = [


    path('', include(router.urls)),

    path('', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.social.urls')),
<<<<<<< HEAD

=======
    
>>>>>>> 04837a0c41a7169f6128130fddc92ae0de2742fa
    #path('promote/', PromoteToVoteAdminView.as_view(), name='promote_to_vote_admin'),

    path('logout/', LogoutAPIView.as_view(), name="logout"),

    #path('activate/<uid>/<token>/', activate, name='activate'),



    path('user-me/update/', CustomUserViewset.as_view(), name='patch_user'),
    path('users/activation/<str:email>/<str:code>/', UserActivationView.as_view()),

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
