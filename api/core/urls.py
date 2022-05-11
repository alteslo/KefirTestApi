from core.views import (CurrentUserPUTCHView, CurrentUserView, LoginView,
                        LogoutView, PrivateUsersViewSet, UsersAPIView)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', PrivateUsersViewSet, basename='private')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/users/current/', CurrentUserView.as_view(),
         name='current_user_information'),
    path('user/users/<int:pk>/', CurrentUserPUTCHView.as_view(),
         name='current_user_putch'),
    path('user/users/', UsersAPIView.as_view(),
         name='general_users_information'),
    path("admin/private/", include(router.urls))
]
