from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import (CurrentUserPUTCHView, CurrentUserView,
                        PrivateUsersViewSet, UsersAPIView)
router = DefaultRouter()
router.register('users', PrivateUsersViewSet, basename='private')

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('users/current/', CurrentUserView.as_view()),
    path('users/<int:pk>/', CurrentUserPUTCHView.as_view()),
    path('users/', UsersAPIView.as_view()),
    path("private/", include(router.urls))
]
