from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import Conversation, Messages
from .serializers import ConversationSerializers, MessagesSerializers

from django.contrib.auth.models import User

class ConversationView(APIView):
    
    def get(self, request, *args, **kwargs):
        conversation = Conversation.objects.filter(members=request.user)
        serializer = ConversationSerializers(conversation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ConversationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleConversationView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['id'])
        conversation = Conversation.objects.filter(members=user).first()
        serializer = ConversationSerializers(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MessageView(APIView):
    
    def get(self, request, *args, **kwargs):
        convo = request.query_params.get('convo', None)
        messages = Messages.objects.filter(conversation=convo)
        serializer = MessagesSerializers(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = MessagesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


