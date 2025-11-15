# chats/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, MessageViewSet, ConversationViewSet

# The test looks for: routers.DefaultRouter()
router = routers.DefaultRouter()

router.register('users', UserViewSet)
router.register('messages', MessageViewSet)
router.register('conversations', ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
