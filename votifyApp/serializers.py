from rest_framework import serializers

from .models import *
from authentication.models import User


class OptionSerializer(serializers.ModelSerializer):
    related_election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all(),required=True)

    class Meta:
        model = Option
        fields = ['id','code','full_name','related_election','vote_counter','creator'] #related_election
        read_only_fields = ['id','creator','vote_counter']
        depth = 1
    
       
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
     class Meta:
        model = VoteAdminRequest
        fields = ['id','creator', 'subject','message','is_validated','created_at']
        read_only_fields = ['id','creator','created_at','is_validated']
        depth = 1
        
        
class NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model = Notification
        fields = ['id','notif_type', 'notif_content','notif_read_status','sent_on']
        read_only_fields = ['id','sent_on']

    

    

