from rest_framework import pagination, permissions, viewsets, generics
from rest_framework.response import Response

from core.models import MyUser
from core.serializers import UsersSerializer, CurrentUsersSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'size'
    ordering = 'date_joined'


class UsersViewSet(viewsets.ModelViewSet):
    '''Постраничное получение кратких данных обо всех пользователях'''

    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberSetPagination


class CurrentUserView(generics.GenericAPIView):
    '''Информация, доступная пользователю о самом себе'''

    serializer_class = CurrentUsersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            "user": CurrentUsersSerializer(
                request.user, context=self.get_serializer_context()
            ).data,
        })
