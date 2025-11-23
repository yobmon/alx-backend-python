# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
# chats/views.py

from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model

from .permissions import IsConversationMember
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProtectedView(APIView):
    """
    A simple ViewSet for testing protected endpoint.
    Accessible only to authenticated users.
    """
    def list(self, request):
        return Response({"message": "This is a protected endpoint accessible only to authenticated users."})
class RegisterView(APIView):
    """User signup"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Missing username or password"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
    



class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles listing, creating, updating, deleting messages
    in a conversation. Only participants can access.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwnerOrReadOnly]

    def get_queryset(self):
        # 1️⃣ Get conversation_id from URL kwargs
        conversation_id = self.kwargs.get("conversation_pk")
        
        # 2️⃣ Ensure the conversation exists
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # 3️⃣ Check if the user is a participant
        if self.request.user not in conversation.participants.all():
            # 4️⃣ Return empty queryset if not allowed
            return Message.objects.none()
        
        # 5️⃣ Filter messages by conversation_id
        return Message.objects.filter(conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Check participant access
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN,  # 6️⃣ Explicit 403
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=False, methods=["post"])
    def create_conversation(self, request):
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response(
                {"error": "participants list is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        conversation.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )
    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        message_body = request.data.get("message_body", "")
        sender_id = request.data.get("sender")

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender_id,
            message_body=message_body
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
    permission_classes = [IsAuthenticated, IsConversationMember]

