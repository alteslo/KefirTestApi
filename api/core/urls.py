from django.urls import include, path
from rest_framework.routers import DefaultRouter
from core.views import MyUserViewSet

router = DefaultRouter()
router.register('users', MyUserViewSet, basename='users')

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),
]
