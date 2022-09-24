from turtle import pos
from django.contrib.auth.models import User
from .serializers import (
                        PostSerializer)
from .models import Post
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os


class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, id):
        post = None
        try:
            post = Post.objects.get(id=id)
        except Exception as e:
            pass
        return post
    
    def get(self, request, *args, **kwargs):
        post_id = kwargs['id']
        post = self.get_object(post_id)

        if post is None:
            return Response({"succes": False, "message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        post = self.get_object(kwargs['id'])
        if post is None:
            return Response({"succes": False, "message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if post.user != request.user:
            return Response({"succes": False, "message": "You can not update other user post"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, *args, **kwargs):
        post = self.get_object(kwargs['id'])

        if post.user != request.user:
            return Response({"succes": False, "message": "You can not delete other user post"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"succes": True, "message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PostLikeView(APIView):

    def put(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['id'])
        except Post.DoesNotExist:
            return Response({"succes": False, "message": "Post does not exists"}, status=status.HTTP_404_NOT_FOUND)
        
        if not post.likes.filter(id=request.user.id).exists():
            post.likes.add(request.user)
            return Response({"succes": True, "message": "Post liked successfully"}, status=status.HTTP_200_OK)
        else:
            post.likes.remove(request.user)
            return Response({"succes": True, "message": "Post unliked successfully"}, status=status.HTTP_200_OK)


class TimelinePostView(APIView):

    def get(self, request, *args, **kwargs):
        current_user_post = Post.objects.filter(user=request.user)
        following_users = request.user.profile.following.values_list('id', flat=True)
        following_users_post = Post.objects.filter(user_id__in=following_users)
        final_qs = current_user_post | following_users_post
        print(following_users_post,'---')
        final_qs = final_qs.order_by('-created_at')
        serializer = PostSerializer(final_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoggedInUserPost(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['id'])
        current_user_post = Post.objects.filter(user=user).order_by('-created_at')
        serializer = PostSerializer(current_user_post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






        

