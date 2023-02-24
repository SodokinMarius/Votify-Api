from rest_framework import serializers

from .models import *
from authentication.models import User
from django.core.validators import FileExtensionValidator


class OptionSerializer(serializers.ModelSerializer):
    related_election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all(),required=True)
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])]
    )
    class Meta:
        model = Option
        fields = ['id','code','full_name','image','related_election','vote_counter','creator'] #related_election
        read_only_fields = ['id','creator','vote_counter']
        depth = 1
        
    def create(self, validated_data):
        image = validated_data.pop('image')
        option = Option.objects.create(**validated_data)
        option.image = image
        option.save()
        return option
       
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id','user', 'voter_type']
        read_only_fields = ['id']


class ElectionSerializer(serializers.ModelSerializer):

    authorized_voters_file = serializers.FileField(allow_null=True,required=True)
    authorized_voters_add = serializers.PrimaryKeyRelatedField(many=True,queryset=Voter.objects.all(),required=False)


    class Meta:
        model = Election
        fields = ['id','title', 'description','authorized_voters_file','authorized_voters_add','date_start','date_end','election_type','turn_number','created_at']
        read_only_fields = ['id','created_at']
        depth = 1
        
    
    def create(self, validated_data):
        authorized_voters_data = validated_data.pop('authorized_voters_add')
        print("Je l'ai supprimé..................>")
        print("voters  sere----------------", authorized_voters_data )

        election = Election.objects.create(**validated_data)

        for voter_data in authorized_voters_data:
            user = User.objects.get(id=voter_data['id'])
            election.authorized_voters.add(user)
        election.save()
        
        return election
        
  
 
class VoteSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vote
        fields = ['id','voter', 'election','choosed_option','created_at']
        read_only_fields = ['id','created_at']
        depth = 1

class VoteAdminRequestSerializer(serializers.ModelSerializer):
    creator_identity_piece = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])]
    )
    class Meta:
        model = VoteAdminRequest
        fields = ['id','creator', 'subject','message','is_validated','created_at', 'creator_identity_piece']
        read_only_fields = ['id','creator','created_at','is_validated']
        depth = 1

    def create(self, validated_data):
        identity_piece = validated_data.pop('creator_identity_piece')
        vote_admin_request = VoteAdminRequest.objects.create(**validated_data)
        vote_admin_request.creator_identity_piece = identity_piece
        vote_admin_request.save()
        return vote_admin_request
        
        
class NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model = Notification
        fields = ['id','notif_type', 'notif_content','notif_read_status','sent_on']
        read_only_fields = ['id','sent_on']

    

    

