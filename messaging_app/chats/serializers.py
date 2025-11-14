from rest_framework import serializers
from .models import User, Message, Conversation

from django.utils.timesince import timesince

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'
class MessageSerializer(serializers.ModelSerializer):

    time_since_sent = serializers.SerializerMethodField()
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()
    class Meta:
        model = Message
        fields ='__all__'
    def get_time_since_sent(self, obj):
        return timesince(obj.sent_at) + " ago"
    def validate_message_body(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Message too short! Must be at least 5 characters.")
        return value
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields ='__all__'