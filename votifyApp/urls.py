from django.urls import path,include
from rest_framework import routers

from .viewsets import *

router = routers.DefaultRouter()


router.register('options',OptionViewSet)

router.register('voters',VoterViewSet)

router.register('votes',VoteViewSet)

router.register('notifications',NotificationViewSet)

router.register('elections',ElectionViewSet)




urlpatterns = router.urls