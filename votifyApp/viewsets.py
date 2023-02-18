import pandas as pd
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from .models import Election, Voter
from .serializers import *
from rest_framework.request import Request
from django.db.models import Q
from django.db.models import Count
from django.http import Http404

from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()


from .models import *
from .permissions import isOwnerOrReadOnly, isVoteAdmin
from .utils.enums import ProgressChoiceEnum, TypeElectionEnum
from .utils.utils import determine_remaining_duration



class OptionViewSet(viewsets.ModelViewSet):   
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin) # Avant de créér une option il faut être un AdminVote
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        election= serializer.validated_data['related_election'] 
        #election = Election.objects.get(id=election_id)
        if election.progress_status == ProgressChoiceEnum.COMPLETED.value:
            return Response({"message" : "Impossible de créer d'options pour une élection terminée !"}, status=status.HTTP_400_BAD_REQUEST)

        elif election.progress_status == ProgressChoiceEnum.IN_PROGESS.value:
            return Response({"message" : "Impossible de créer d'options pour une élection déjà en cours !"}, status=status.HTTP_400_BAD_REQUEST)
 
        elif election.progress_status == ProgressChoiceEnum.CANCELLED.value:
            return Response({"message" : "Impossible de créer d'options pour une élection annulée !"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.validated_data['creator'] = user
        
        serializer.save()
    
class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    permission_classes = (permissions.IsAuthenticated, isVoteAdmin)
    

class ElectionViewSet(viewsets.ModelViewSet):  
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super(ElectionViewSet, self).get_serializer_context()
        context['request'] = self.request
        print("Le contexte--------------",context)
        return context

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        print("Cllling serializer-------->",kwargs['context'] )
        return super(ElectionViewSet, self).get_serializer(*args, **kwargs)
    
    
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
            voters = []
            voters_email = {
                "subscribed":"",
                "unsubscribed":""
                }
            anonymous_voters =  ""
            for email in df['email']:
                
                print("Mail trouvé dans le fichier ------->",email)
                try:
                    user = User.objects.get(email=email)
                    voter = Voter.objects.create(user=user)
                    print("New Voter------------>",voter)
                    voters.append(voter)
                    message = "Vous êtes invité à participer à l'élection: {} crée par {}".format(election.title,self.request.user)
                    
                    # send notification to existing voter
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email= from_email,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    voters_email["subscribed"] += email+' ' #Save the user Mail

                  
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
                    voters_email["unsubscribed"] += email +' ' # Add to email list in the database when user doesn't login

                    continue
            
            #Creation de la notification dans le table Notification
                
                Notification.objects.create(
                    notif_type=subject,
                    notif_content="Une nouvelle élection de titre {}  vient d'être crée par {}".format(election.title,self.request.user),
                    notif_read_status=False,                    
                )
            election.authorized_voters.set(voters)

        """#Options treating before saving the elections    
        options = []
        option_data = []
        try:
            options_data = self.request.data.getlist('options')
            options_data = json.dumps(option_data)
            print("La liste des options ==== try =============",option_data)

        except :
            options_data = [{"IFRI","Marius"},{"EPAC",'SOD'},]
            
      
        print("La liste des options =================",option_data)
        for option_data in options_data:
            # Créer une instance Option pour chaque option entrée par l'utilisateur
            option_serializer = OptionSerializer(data=option_data)
            option_serializer.is_valid(raise_exception=True)
            option = option_serializer.save(creator=self.request.user)
            options.append(option)

        # Ajouter les options à l'objet Election avant de le valider
        serializer.validated_data['options'] = options
        serializer.validated_data['creator'] = self.request.user"""
        serializer.save()
        
        # save the election after processing the excel file
        election.voters_email = voters_email
        election.creator = self.request.user
        election.save()
        
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
 
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
            emails = election.voters_email
            print('Les emails ------->',emails)

            autorized_voters = list(election.authorized_voters.all())
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
        Q(progress_status=retrieved_status)
        ).order_by('-created_at')
    
        private_elections = self.queryset.filter(
        Q(progress_status=retrieved_status) &
        Q(election_type=TypeElectionEnum.PRIVATE.value)
        ).order_by('-created_at')
        
        print("Private",private_elections,"Public ===",public_elections)

        authorized_private_elections = []
        for election in private_elections:
            autorized_voters = list(election.authorized_voters.all())
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

    """
    This function take an election status parameter an set the conserned election to this status
    Before make chages, we verify if the election is alredy to procided status 
    IF status is to sart we verify the current date is included in election date interval again
    A started or alredy cancelled or completed election can not be cancelled
    """
    def changeElectionStatus(self, change_to:str):
        election = self.get_object()
        current_date = timezone.now()
        response ={}
        if (
            election.progress_status == change_to 
            or 
            (election.progress_status == (
                ProgressChoiceEnum.IN_PROGESS.value or ProgressChoiceEnum.COMPLETED.value)
             and change_to == ProgressChoiceEnum.CANCELLED.value)
        ):
            response = {"message" : "This election can not be set to this status"}
            print("le election cliqué :{} et ses options : {}".format(election,Option.objects.filter(related_election=election).count()))
        elif Option.objects.filter(related_election=election).count() <= 0 and change_to == ProgressChoiceEnum.IN_PROGESS.value:
            print("le election cliqué :{} et ses options : {}".format(election,Option.objects.filter(related_election=election).count()))
            response = {"message" : "Veuillez créer au moins deux options de l'election avant de demarrer !"} # On ne peut pas demarrer une eection sans créer au moin deux de ces options

        else:
            election.progress_status = change_to
            if change_to == ProgressChoiceEnum.CANCELLED.value:
                election.is_cancelled = True
            elif change_to == ProgressChoiceEnum.COMPLETED.value:
                election.date_end = current_date
            elif change_to == ProgressChoiceEnum.IN_PROGESS.value:
                election.date_start = current_date

            election.save()
            serializer = ElectionSerializer(election)
            response = {
                'data' : serializer.data,
                'message' : "Election has been changed successfully  to {}!".format(change_to)
            }
        return response

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
        This function return cancelled election : public and private if there is
    Returns:
        _type_: Election list    """
    
    @action(methods=['get'], detail=False, url_path="cancelled", url_name="cancelled")
    def cancelled(self, request):
        
        response_data = self.getAllElectionCategorizedByStatus(ProgressChoiceEnum.CANCELLED.value)    
    
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    
    """
        Methods that start an election after admin clic on Start buuton on frontend
    """

    @action(detail=True,methods=['get'],url_path="start", url_name="start")
    def start(self, request, pk=None):        
        response = self.changeElectionStatus(ProgressChoiceEnum.IN_PROGESS.value)
        return Response(data=response)

    """
    Methods that MAKE COMPLETE an election after admin clic on MAKE COMPLETE buuton on frontend
    """

    @action(detail=True,methods=['get'],url_path="complete", url_name="complete")
    def complete(self, request, pk=None):        
        response = self.changeElectionStatus(ProgressChoiceEnum.COMPLETED.value)
        return Response(data=response)
    
    """
    Methods that MAKE CANCELLED an election after admin clic on MAKE CANCELLED buuton on frontend
    """
    @action(detail=True,methods=['get'],url_path="cancel", url_name="cancel")
    def cancel(self, request, pk=None):        
        response = self.changeElectionStatus(ProgressChoiceEnum.CANCELLED.value)
        return Response(data=response)

    
    
    """@action(detail=True, methods=['get'], url_path="vote/(?P<option_code>[^/.]+)", url_name="vote")
    def vote(self,request,**kwargs):
        user_id = self.request.user
        election_id = self.kwargs['pk']

        #election = self.get_object() # Get the currently requested Election instance
        option_code = ""
        election = 0
        try:
            option_code = self.kwargs['option_code']
            election = Election.objects.get(id=election_id)
        except Option.DoesNotExist:
            raise Http404("Option does not exist")
        

        print("option id-------------",option_code)

        # Check if voter and election exist
        voter = ""
        election = ""
        try:
            user = User.objects.get(email=user_id)
            voter = Voter.objects.get(user=user)
            #election = Election.objects.get(id=election_id)
        except (Voter.DoesNotExist, Election.DoesNotExist):
            return Response({'message': 'Invalid voter or election Vt{} et El{}'.format(self.request.user,election)}, status=status.HTTP_400_BAD_REQUEST)

        # Check if option exists and is for this specific election
        try:
            print("Cet option id ==========",option_code)
            option = Option.objects.get(code=option_code, related_election=election)
        except Option.DoesNotExist:
            return Response({'message': 'Invalid option ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the voter has already voted in this election
        if Vote.objects.filter(voter=voter, election=election).count() >= election.turn_number:
            return Response({'message': 'Vous avez déjà terminé les votes relatives à cette election'}, status=status.HTTP_400_BAD_REQUEST)

        option.vote_counter += 1
        vote = Vote.objects.create(voter=voter, election=election, choosed_option=option)

        return Response({'message': 'Vote registered successfully', 'vote_id': vote.id}, status=status.HTTP_201_CREATED)"""
        
    @action(detail=True, methods=['get'], url_path="vote/(?P<option_id>[^/.]+)", url_name="vote")
    def vote(self, request, option_id, **kwargs):
        user_id = self.request.user
        election = self.get_object()
        option = None

        # Check if voter and election exist
        try:
            user = User.objects.get(email=user_id)
            voter = Voter.objects.get(user=user)
        except Voter.DoesNotExist:
            return Response({'message': 'Invalid voter'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if option exists and is for this specific election
        try:
            option = Option.objects.get(id=option_id, related_election=election)
        except (Option.DoesNotExist, ValueError):
            return Response({'message': 'Invalid option ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the voter has already voted in this election
        if Vote.objects.filter(voter=voter, election=election).count() >= election.turn_number:
            return Response({'message': 'Vous avez déjà terminé les votes relatives à cette election'}, status=status.HTTP_400_BAD_REQUEST)
        print("Option ::",option)
        if option.vote_counter is None:
            option.vote_counter = 0
        option.vote_counter += 1
        option.save()
        vote = Vote.objects.create(voter=voter, election=election, choosed_option=option)

        return Response({'message': 'Vote registered successfully', 'vote_id': vote.id}, status=status.HTTP_201_CREATED)

        
    

    @action(detail=True, methods=['get'], url_path='stats', url_name='stats')
    def election_stats(self, request, pk=None):
        # Get the Election object
        election = self.get_object()

        # Check if the election is closed
        if election.progress_status != ProgressChoiceEnum.COMPLETED.value:
            return Response({'message': 'Cette election est toujours en cours'}, status=status.HTTP_400_BAD_REQUEST)
        elif election.progress_status == ProgressChoiceEnum.CANCELLED.value:
            return Response({'message': 'Cette election a été annulée !'}, status=status.HTTP_400_BAD_REQUEST)
        elif election.progress_status == ProgressChoiceEnum.PENDING.value:
            return Response({"message": "Cette election n'est pas encore démarré !"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the total number of voters
        voters_count = Vote.objects.filter(election=election).values('voter').distinct().count()

        # Get the option with the highest vote count
        winning_option = Option.objects.filter(related_election=election).annotate(num_votes=Count('vote')).order_by('-num_votes').first()

        # Calculate the winning option's percentage of the total votes
        if winning_option is not None:
            winning_percentage = 100 * winning_option.num_votes / Vote.objects.filter(election=election).count()
        else:
            winning_percentage = 0

        # Construct the response data
        response_data = {
            'title': election.title,
            'description': election.description,
            'winning_option': winning_option.full_name if winning_option else None,
            'winning_option_score': winning_option.num_votes if winning_option else 0,
            'winning_option_percentage': winning_percentage,
            'num_voters': voters_count
        }

        return Response(response_data, status=status.HTTP_200_OK)



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
      
    
  

  
