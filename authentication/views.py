from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import User

from .serializers import LogoutSerializer

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

from dj_rest_auth.registration.views import SocialLoginView

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from .serializers import  UserCreateSerializer



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter



class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated(),)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = request.data
        user = request.user
        setattr(user,'actual_connected_espace',None)
        user.save()

        return Response(data=data,status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class =  UserCreateSerializer

    @action(detail=True, methods=['get'])
    def subscribe(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        subscriber = request.user
        user.subscribers.add(subscriber)
        user.save()
        return Response({'status': 'subscribed'})  
    
