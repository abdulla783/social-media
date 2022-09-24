from django.urls import path
from .views import (
                    RegisterView, 
                    LoginView, 
                    UserProfileView, 
                    ChangePasswordView, 
                    GetUserInformationsView, 
                    FollowersView,
                    UnFollowView,
                    UploadImageAndCover,
                    UserFollowings)

app_name = "account"

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile_view'),
    path('profile/image-upload', UploadImageAndCover.as_view(), name='profile_image_upload'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('user-profile/<int:id>', GetUserInformationsView.as_view(), name='user_profile'),
    path('follow/<int:id>', FollowersView.as_view(), name='follow'),
    path('unfollow/<int:id>', UnFollowView.as_view(), name='unfollow'),
    path('user-followings/<int:id>', UserFollowings.as_view(), name='my-followings')

]
