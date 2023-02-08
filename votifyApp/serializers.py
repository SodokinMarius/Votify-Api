from rest_framework import serializers

from .models import *


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id','code','full_name','related_election',]
        read_only_fields = ['id']
    
       
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id','user', 'voter_type']
        read_only_fields = ['id']


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['id','title', 'description','date_start','date_end','election_type','turn_number']
        read_only_fields = ['id']


class VoteSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vote
        fields = ['id','voter', 'election','choosed_option','created_at']
        read_only_fields = ['id','created_at']


class NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vote
        fields = ['id','notif_type', 'notif_content','notif_read_status','sent_on']
        read_only_fields = ['id','sent_on']

    

    

