from djoser.serializers import UserCreateSerializer,UserCreatePasswordRetypeSerializer

from .models import User
from rest_framework import serializers
from djoser import serializers as djoser_serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from  .config import SITE_NAME

class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ['username','email','first_name','last_name','address','phone','password']         
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1
    
  
class CustomUserSerializer(djoser_serializers.UserSerializer):
    def send_confirmation(self):
       
        subject = f'Activation de compte sur {SITE_NAME}'
       
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.refresh_token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            self.fail('bad_token')

