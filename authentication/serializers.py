
from djoser.serializers import UserCreateSerializer as DjoserUserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers

from votifyApp.utils import send_email 
from votifyApp.utils import random_generate
from django.core.validators import FileExtensionValidator


User = get_user_model()

class UserCreateSerializer(DjoserUserSerializer):
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])]
        
    )
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ['username','email','first_name','last_name','address','phone', 'image','password','is_vote_admin']  
        read_only_fields = ('is_vote_admin',)      
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1
        
    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")
    
    def create(self, validated_data):
        image = validated_data.pop('image')
        user = User.objects.create(**validated_data)
        user.image = image
        user.save()        
        return user

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

