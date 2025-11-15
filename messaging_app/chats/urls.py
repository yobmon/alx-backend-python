# chats/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, MessageViewSet, ConversationViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('users', UserViewSet)
router.register('messages', MessageViewSet)
router.register('conversations', ConversationViewSet)

nested_router = routers.NestedDefaultRouter(router, 'conversations', lookup='conversation')
nested_router.register('messages', MessageViewSet, basename='conversation-messages')
urlpatterns = [
    path('', include(router.urls)),
      path('', include(nested_router.urls)),
]
