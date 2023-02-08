from djoser.serializers import UserCreateSerializer as DjoserUserSerializer,UserCreatePasswordRetypeSerializer

from django.contrib.auth import get_user_model

from .models import User

from rest_framework import serializers
from djoser import serializers as djoser_serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from  .config import SITE_NAME

#User = get_user_model()
class UserCreateSerializer(DjoserUserSerializer):
    
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ['username','email','first_name','last_name','address','phone','password']        
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1
        
'''class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ['username','email','first_name','last_name','address','phone','password']        
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1

    
    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")'''

        

  
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

