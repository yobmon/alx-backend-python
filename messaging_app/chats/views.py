from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all(is_staff=True)
    serializer_class = UserSerializer
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
class MessageViewSet(viewsets.ModelViewSet):
   
    queryset = Message.objects.all().order_by('-sent_at')

    serializer_class= ConversationSerializer
