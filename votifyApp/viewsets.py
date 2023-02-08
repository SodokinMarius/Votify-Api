from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from authentication.models import User

from rest_framework import permissions


from .permissions import(
    isOwnerOrReadOnly,
    isVoteAdmin,
)

from .models import *

from .utils.enums import  ProgressChoiceEnum
from .utils.utils import (
    determine_remaining_duration)


class OptionViewSet(viewsets.ModelViewSet):   
    queryset = Option.objects.all()
    serialiser_class = OptionSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)
    #http_method_names = ['GET','POST']
    
    

class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)



class ElectionViewSet(viewsets.ModelViewSet):  
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)
  

class VoteViewSet(viewsets.ModelViewSet):  
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)


class NotificationViewSet(viewsets.ModelViewSet):  
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)
  

  
