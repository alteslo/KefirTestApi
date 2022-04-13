from django.urls import include, path
from rest_framework.routers import DefaultRouter
from core.views import UsersViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),
]
