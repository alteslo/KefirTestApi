from rest_framework import (generics, mixins, pagination, permissions, status,
                            viewsets)
from rest_framework.response import Response

from core.models import MyUser
from core.permissions import IsOwnerOrReadOnly, MyIsAdmin
from core.serializers import (CurrentUsersPUTCHSerializer,
                              CurrentUsersSerializer,
                              PrivateGETUsersSerializer,
                              PrivateLISTUsersSerializer, UsersSerializer)


class PageNumberSetPagination(pagination.PageNumberPagination):
    """
    Простой пагинатор, который поддерживает номера страниц
    как параметры запроса. Например:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&size=100
    """

    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'size'
    ordering = 'date_joined'

    def get_paginated_response(self, data):
        query_size = self.request.query_params.get('size')

        if query_size is None:
            query_size = self.page_size

        return Response({
            'data': data,
            "meta": {
                'pagination': {
                    'total': self.page.paginator.num_pages,
                    'page': self.page.number,
                    'size': int(query_size)
                }
            },
        })


class UsersAPIView(generics.ListAPIView):
    '''Постраничное получение кратких данных обо всех пользователях'''

    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = PageNumberSetPagination


class CurrentUserView(generics.GenericAPIView):
    '''Информация, доступная пользователю о самом себе'''

    serializer_class = CurrentUsersSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response({
            'user': CurrentUsersSerializer(
                request.user, context=self.get_serializer_context()
            ).data,
        })


class CurrentUserPUTCHView(mixins.UpdateModelMixin, generics.GenericAPIView):
    '''Изменение данных пользователя'''

    serializer_class = CurrentUsersPUTCHSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = MyUser.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PrivateUsersViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    '''Пользовательский viewset поддерживающий CRUD методы'''

    queryset = MyUser.objects.all()
    serializer_class = PrivateGETUsersSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = (permissions.IsAuthenticated, MyIsAdmin)

    def list(self, request, *args, **kwargs):
        '''Краткая информация обо всех пользователях'''

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PrivateLISTUsersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PrivateGETUsersSerializer(page, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        if 'password' in request.data.keys():
            data = {"code": 400, "message": "Изменение пароля не разрешено"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        '''Изменение информации о пользователе'''

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
