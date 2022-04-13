from django.urls import include, path
from rest_framework.routers import DefaultRouter
from core.views import UsersViewSet, CurrentUserView

router = DefaultRouter()
router.register('', UsersViewSet, basename='users')

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('users/current/', CurrentUserView.as_view()),
    path('users/', include(router.urls)),
]
