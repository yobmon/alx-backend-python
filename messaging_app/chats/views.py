# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer


# -----------------------------
# User ViewSet
# -----------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# -----------------------------
# Message ViewSet
# -----------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


# -----------------------------
# Conversation ViewSet
# -----------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    # -------------------------
    # Endpoint to create a new conversation
    # POST /conversations/create_conversation/
    # -------------------------
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

    # -------------------------
    # Endpoint to send message to existing conversation
    # POST /conversations/<id>/send_message/
    # -------------------------
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
