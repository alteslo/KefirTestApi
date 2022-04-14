from django.urls import include, path

from core.views import CurrentUserView, UsersAPIView, CurrentUserPUTCHView


urlpatterns = [
    path('', include('rest_framework.urls')),
    path('users/current/', CurrentUserView.as_view()),
    path('users/<int:pk>/', CurrentUserPUTCHView.as_view()),
    path('users/', UsersAPIView.as_view()),
]
