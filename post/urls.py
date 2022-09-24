from django.urls import path
from .views import (
                    PostView, 
                    PostDetailView, 
                    PostLikeView, 
                    TimelinePostView,
                    LoggedInUserPost
                    )

app_name = "post"

urlpatterns = [
    path('', PostView.as_view(), name='post_list'),
    path('<int:id>', PostDetailView.as_view(), name='post_details'),
    path('like/<int:id>', PostLikeView.as_view(), name='post_like'),
    path('timeline', TimelinePostView.as_view(), name='post_timeline'),
    path('myposts/<int:id>', LoggedInUserPost.as_view(), name='myposts')
]
