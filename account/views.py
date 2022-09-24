from django.contrib.auth.models import User
from .serializers import (
                        RegisterSerializer, 
                        LoginSerializer, 
                        ProfileUpdateSerializer, 
                        ChangePasswordSerializer,
                        ProfileImageUploadSerializer,
                        )
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os


BASE_TEMP = os.path.join(settings.BASE_DIR, 'temp')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'success': True,
                "status_code": status.HTTP_200_OK,
                "message": "user logged in successfully",
                "access": serializer.data['access'],
                "refresh": serializer.data['refresh'],
                "id": serializer.data['id'],
                "username": serializer.data['username'],
                "email": serializer.data['email'],
                "profile_image": serializer.data['profile_image'],
                "following": serializer.data['following']
            }, status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileUpdateSerializer(user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        data = request.data
        print(data,'data')
        serializer = ProfileUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadImageAndCover(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)
    
    def patch(self, request, *args, **kwargs):
        data = request.data
        serializer = ProfileImageUploadSerializer(request.user.profile, data=data)
        if serializer.is_valid():
            serializer.save()            
        print(serializer.errors)
        return Response({}, status=status.HTTP_200_OK)


class GetUserInformationsView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        try:
            user = User.objects.get(id=user_id)
            serializer = ProfileUpdateSerializer(user.profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)




class ChangePasswordView(generics.UpdateAPIView):
    '''
    View to change a logged in user password
    '''
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        '''
        Method to Update the logged user password
        : Mehod : `PUT`
        : Permission : 'Only Authenticated and Logged in user'
        : Params : `Old Password, New Password`
        : Response : `Success Message with 200 status code`

        '''

        try:
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            return Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'Warning': "Old password does not match with our system"}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'Success',
                'code': status.HTTP_200_OK,
                'message': "Password changed successfully"
            }
            return Response(response)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Following and Followers API

class FollowersView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        if request.user.id != kwargs['id']:
            try:
                user = User.objects.get(id=kwargs['id'])
                current_user = request.user
                if not user.profile.followers.filter(id=current_user.id).exists():
                    user.profile.followers.add(current_user)
                    user.profile.save()
                    current_user.profile.following.add(user)
                    current_user.profile.save()
                    return Response({"succes": True, "message": "Followed"}, status=status.HTTP_200_OK)
                else:
                    return Response({"succes": False, "message": "Already followed"}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"succes": False, "message": "You can't follow your self"}, status=status.HTTP_403_FORBIDDEN)

class UnFollowView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        if request.user.id != kwargs['id']:
            try:
                user = User.objects.get(id=kwargs['id'])
                current_user = request.user
                if user.profile.followers.filter(id=current_user.id).exists():
                    user.profile.followers.remove(current_user)
                    user.profile.save()
                    current_user.profile.following.remove(user)
                    current_user.profile.save()
                    return Response({"succes": True, "message": "UnFollowed"}, status=status.HTTP_200_OK)
                else:
                    return Response({"succes": False, "message": "Already unfollowed"}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"succes": False, "message": "You can't unfollow your self"}, status=status.HTTP_403_FORBIDDEN)

class UserFollowings(APIView):

    def get(self, request, *arg, **kwargs):
        user_data = []
        followings = User.objects.get(id=kwargs['id']).profile.following.all()
        for follow in followings:
            user_data.append({
                "username": follow.username,
                "first_name": follow.first_name,
                "last_name": follow.last_name,
                "id": follow.id,
                'profile_image': follow.profile.profile_image.url if follow.profile.profile_image else ""
            })
        print(followings)
        return Response(user_data, status=status.HTTP_200_OK)

