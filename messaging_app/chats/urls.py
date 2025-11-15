
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,MessageViewSet,ConversationViewSet
#  router.DefaoultRouter()
router = DefaultRouter()
router.register('users', UserViewSet)

router.register('messages', MessageViewSet)
router.register('conversations', ConversationViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
