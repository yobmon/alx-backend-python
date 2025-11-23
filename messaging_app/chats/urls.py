# chats/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import (
    UserViewSet,
    MessageViewSet,
    ConversationViewSet,
    RegisterView,
    ProtectedView,
)

# JWT Authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('messages', MessageViewSet)
router.register('conversations', ConversationViewSet)

nested_router = NestedDefaultRouter(
    router,
    'conversations',
    lookup='conversation'
)
nested_router.register(
    'messages',
    MessageViewSet,
    basename='conversation-messages'
)

urlpatterns = [

   
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
