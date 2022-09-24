from rest_framework import serializers
from .models import Conversation, Messages


class ConversationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class MessagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'