from rest_framework import serializers

from .models import *


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id','code','full_name','related_election','created_by']
        read_only_fields = ['id','created_by']
    
       
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id','user', 'voter_type']
        read_only_fields = ['id']


class ElectionSerializer(serializers.ModelSerializer):
    authorized_voters_file = serializers.FileField(allow_null=True, required=False)
    authorized_voters_add = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Election
        fields = ['id','title', 'description','authorized_voters_file','authorized_voters_add','date_start','date_end','election_type','turn_number']
        read_only_fields = ['id']


class VoteSerializer(serializers.ModelSerializer):
     class Meta:
        model = Vote
        fields = ['id','voter', 'election','choosed_option','created_at']
        read_only_fields = ['id','created_at']


class NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model = Notification
        fields = ['id','recipient','notif_type', 'notif_content','notif_read_status','sent_on']
        read_only_fields = ['id','sent_on','recipient']

    

    

