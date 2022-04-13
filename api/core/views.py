from rest_framework import pagination, permissions, viewsets

from core.models import MyUser
from core.serializers import UsersSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'size'
    ordering = 'created_at'


class UsersViewSet(viewsets.ModelViewSet):
    '''Постраничное получение кратких данных обо всех пользователях'''

    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberSetPagination
