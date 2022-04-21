from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import (CurrentUserPUTCHView, CurrentUserView,
                        PrivateUsersViewSet, UsersAPIView)
router = DefaultRouter()
router.register('users', PrivateUsersViewSet, basename='private')

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('user/users/current/', CurrentUserView.as_view()),
    path('user/users/<int:pk>/', CurrentUserPUTCHView.as_view()),
    path('user/users/', UsersAPIView.as_view()),
    path("admin/private/", include(router.urls))
]
