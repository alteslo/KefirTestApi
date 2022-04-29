from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import (CurrentUserPUTCHView, CurrentUserView, LoginView,
                        LogoutView, PrivateUsersViewSet, UsersAPIView)

router = DefaultRouter()
router.register('users', PrivateUsersViewSet, basename='private')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/users/current/', CurrentUserView.as_view()),
    path('user/users/<int:pk>/', CurrentUserPUTCHView.as_view()),
    path('user/users/', UsersAPIView.as_view(),
         name='general_users_information'),
    path("admin/private/", include(router.urls))
]
