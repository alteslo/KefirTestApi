from core.models import Cities, MyUser
from core.permissions import IsOwnerOrReadOnly, MyIsAdmin
from core.serializers import (CurrentUsersPUTCHSerializer,
                              CurrentUsersSerializer,
                              PrivateGETUsersSerializer,
                              PrivateLISTUsersSerializer, UsersSerializer)
from django.contrib.auth import authenticate, login, logout
from rest_framework import (generics, mixins, pagination, permissions, status,
                            viewsets)
from rest_framework.response import Response


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


class LoginView(generics.GenericAPIView):
    '''Вход в систему'''

    serializer_class = CurrentUsersSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        data = request.data

        username = data.get('login', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                serializer = self.get_serializer(user)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.GenericAPIView):
    '''Выход из системы'''

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class CurrentUserView(generics.GenericAPIView):
    '''Информация, доступная пользователю о самом себе'''

    serializer_class = CurrentUsersSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserPUTCHView(mixins.UpdateModelMixin, generics.GenericAPIView):
    '''Изменение данных пользователя'''

    serializer_class = CurrentUsersPUTCHSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = MyUser.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer_fields = list(serializer.fields.keys())
        for data_field in request.data.keys():
            if data_field not in serializer_fields:
                data = {
                    'code': 400,
                    'message': f'Изменение {data_field} не разрешено'
                }
                return Response(data, status.HTTP_400_BAD_REQUEST)
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
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        '''Изменение информации о пользователе'''

        if 'password' in request.data.keys():
            data = {"code": 400, "message": "Изменение пароля не разрешено"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if 'city' in request.data.keys():
            city = request.data.get('city')
            if Cities.objects.filter(city=city).exists() is False:
                Cities.objects.create(city=city)

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
