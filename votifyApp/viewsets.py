import pandas as pd
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Election, Voter
from .serializers import *
from rest_framework.request import Request
from django.db.models import Q


User = get_user_model()


from .models import *
from .permissions import isOwnerOrReadOnly, isVoteAdmin
from .utils.enums import ProgressChoiceEnum, TypeElectionEnum
from .utils.utils import determine_remaining_duration



class OptionViewSet(viewsets.ModelViewSet):   
    queryset = Option.objects.all()
    serialiser_class = OptionSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin) # Avant de créér une option il faut être un AdminVote
    
    
    

class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)
  


class ElectionViewSet(viewsets.ModelViewSet):  
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    
    """
    Must be Vote Admin and Authenticated before create an Election
    """
    def get_permissions(self):
        method = self.request.method
        if  method in ('PUT', 'PATCH','POST'):
           return [permissions.IsAuthenticatedOrReadOnly(),isVoteAdmin()]
        else  :    
            return [permissions.IsAuthenticated()]

    """
    Method that personalize the an election creation by treating an xlsx file with pandas
    """
    def perform_create(self, serializer):
        election = serializer.save()
        file = self.request.FILES.get('authorized_voters_file')
        if file:
            # read the excel file using pandas
            df = pd.read_excel(file)
            # check if there is a column 'email'
            if 'email' not in df.columns:
                raise ValidationError({'error': 'The excel file must contain a column named "email"'})
            # check if there are any empty cells in the 'email' column
            if df['email'].isnull().sum() > 0:
                raise ValidationError({'error': 'The "email" column cannot contain empty cells'})
            # loop through the email addresses and check if they exist in the Voter model
            subject = NotificationTypeEnum.NEW_VOTE.value
            from_email = "yaomariussodokin@gmail.com"

            for email in df['email']:
                try:
                    user = User.objects.get(email=email)
                    voter = Voter.objects.get(user=user)
                    election.authorized_voters_add.add(voter)
                    message = "Vous êtes invité à participer à l'élection: {}".format(election.title)
                    
                    # send notification to existing voter
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email= from_email,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Voter.DoesNotExist:
                    # send notification to new voter
                    send_mail(
                        subject=subject,
                        massage=f'A new election has been created. Please download the application and register with this email address to get your unique vote code.',
                        from_email=from_email,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except User.DoesNotExist:
                    raise ValidationError("L'utilisaeteur n'existe pas ")
        # save the election after processing the excel file
        election.creator = self.request.user
        election.save()

 
    """_summary_
    - this function is for getting the all list of Election (private or public), whatever the status
    - All completed Election public or private
    - Fillter all private vote in retrieved list
    - If vote is private : if the current connnect user is conserned for the vote or is the vote creator,he will se the list
    - else he see only public votes
    Returns:
        _type_: _description_
    """
    def list(self, request, *args, **kwargs):
        user = request.user
        public_elections = self.queryset.filter(election_type=TypeElectionEnum.PUBLIC.value)
        private_elections = self.queryset.filter(election_type=TypeElectionEnum.PRIVATE.value)

        authorized_private_elections = []
        for election in private_elections:
            autorized_voters = list(election.authorized_voters_add.all())
            print("Autorized voter", autorized_voters,"User--------",user)
            print("'Creator==========+++>",election.creator)

            if user in autorized_voters   or election.creator == user:
                authorized_private_elections.append(election)
        
        public_elections_serializer = ElectionSerializer(public_elections, many=True)
        private_elections_serializer = ElectionSerializer(authorized_private_elections, many=True)
        
        response_data = {
            'public_elections': public_elections_serializer.data,
            'private_elections': private_elections_serializer.data,
        }
        
        return Response(data=response_data, status=status.HTTP_200_OK)

    """_summary_
    THis function take a election status as parameter and returns 
    all Elections whatever the type after treating
    """
    
    def getAllElectionCategorizedByStatus(self,retrieved_status):
        print("Param : ",retrieved_status, "Choice :",ProgressChoiceEnum.PENDING.value)
        
        public_elections = self.queryset.filter(
        Q(election_type=TypeElectionEnum.PUBLIC.value) &
        Q(progress_status=ProgressChoiceEnum.PENDING.value)
        ).order_by('-created_at')
    
        private_elections = self.queryset.filter(
        Q(progress_status=ProgressChoiceEnum.PENDING.value) &
        Q(election_type=TypeElectionEnum.PRIVATE.value)
        ).order_by('-created_at')
        
        print("Private",private_elections,"Public ===",public_elections)

        authorized_private_elections = []
        for election in private_elections:
            autorized_voters = list(election.authorized_voters_add.all())
            print("Autorized voter-----------ff", autorized_voters,"User--------",self.request.user)
            print("'Creator==========+++  yyy-->",election.creator)
            print("Test-----------------------------------,",election.creator == self.request.user)

            if self.request.user in autorized_voters or election.creator == self.request.user:
                print("ouiii-----------------------------------,",election.creator == self.request.user)
                authorized_private_elections.append(election)
        public_elections_serializer = ElectionSerializer(public_elections, many=True)
        private_elections_serializer = ElectionSerializer(authorized_private_elections, many=True)
        
        response_data = {
            'public_elections': public_elections_serializer.data,
            'private_elections': private_elections_serializer.data,
        }
        print("Private",response_data["private_elections"],"Public ===",response_data["public_elections"])
        return response_data

    """_summary_
          This function return completed election : public and private if there is
    Returns:
        _type_: Election list
    """
    
    @action(methods=['get'], detail=False, url_path="completed", url_name="completed")
    def completed(self, request):
        
        response_data = self.getAllElectionCategorizedByStatus(ProgressChoiceEnum.COMPLETED.value)
      
        return Response(data=response_data, status=status.HTTP_200_OK)
    

    """_summary_
            This function return completed election : public and private if there is
        Returns:
            _type_: Election list
        """
    
    @action(methods=['get'], detail=False, url_path="pending", url_name="pending")
    def pending(self, request):
        
        response_data = self.getAllElectionCategorizedByStatus(ProgressChoiceEnum.PENDING.value)    
    
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    
    """_summary_
        This function return In progress election : public and private if there is
    Returns:
        _type_: Election list    """
    
    @action(methods=['get'], detail=False, url_path="in_progress", url_name="in_progress")
    def in_progress(self, request):
        
        response_data = self.getAllElectionCategorizedByStatus(ProgressChoiceEnum.IN_PROGESS.value)    
    
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    
    """_summary_
        This function return Delayed election : public and private if there is
    Returns:
        _type_: Election list    """
    
    @action(methods=['get'], detail=False, url_path="cancelled", url_name="cancelled")
    def cancelled(self, request):
        
        response_data = self.getAllElectionCategorizedByStatus(ProgressChoiceEnum.CANCELLED.value)    
    
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    

class VoteViewSet(viewsets.ModelViewSet):  
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)

    def get_permissions(self):
        method = self.request.method
        if  method in ('PUT', 'PATCH','POST'):
           return [permissions.IsAuthenticatedOrReadOnly(),isOwnerOrReadOnly()]
        else  :    
            return [permissions.IsAuthenticated()]

class NotificationViewSet(viewsets.ModelViewSet):  
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)
    
       
    http_method_names = ['get']
    
    def get_permissions(self):
        method = self.request.method
        if  method in ('PUT', 'PATCH','POST'):
           return [permissions.IsAuthenticatedOrReadOnly(),isOwnerOrReadOnly()]
        else  :    
            return [permissions.IsAuthenticated()]
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.queryset.filter(notif_read_status=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
      
    
  

  
