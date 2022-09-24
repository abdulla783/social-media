from django.urls import path
from .views import (
                   ConversationView,
                   SingleConversationView,
                   MessageView
                    )

app_name = "conversation"

urlpatterns = [
    path('', ConversationView.as_view(), name='conversations_list'),
    path('<int:id>', SingleConversationView.as_view(), name='single_conversation'),
    path('messages', MessageView.as_view(), name='message_view')

]
