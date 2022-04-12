from rest_framework import viewsets
from core.serializers import UserSerializer
from core.models import MyUser


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
