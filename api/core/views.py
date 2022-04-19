from rest_framework import generics, pagination, permissions, status, viewsets
from rest_framework.response import Response

from core.models import MyUser
from core.serializers import (CurrentUsersPUTCHSerializer,
                              CurrentUsersSerializer,
                              PrivateGETUsersSerializer,
                              PrivateLISTUsersSerializer, UsersSerializer)


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'size'
    ordering = 'date_joined'


class UsersAPIView(generics.ListAPIView):
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
            'user': CurrentUsersSerializer(
                request.user, context=self.get_serializer_context()
            ).data,
        })


class CurrentUserPUTCHView(generics.UpdateAPIView):
    '''Информация, доступная пользователю о самом себе'''

    serializer_class = CurrentUsersPUTCHSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MyUser.objects.all()

    def put(self, request, *args, **kwargs):
        data = {"detail": "Метод \"PUT\" не разрешен."}
        return Response(data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk, **kwargs):
        if request.user.id == pk:
            kwargs['partial'] = True
            return self.update(request, pk, **kwargs)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PrivateUsersViewSet(viewsets.ModelViewSet):
    '''Пользовательский viewset поддерживающий CRUD методы'''
    queryset = MyUser.objects.all()
    serializer_class = PrivateGETUsersSerializer
    pagination_class = PageNumberSetPagination
    # permission_classes = [IsAccountAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PrivateLISTUsersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PrivateGETUsersSerializer(page, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        if 'password' in request.data.keys():
            data = {"code": 400, "message": "Изменение пароля не разрешено"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
