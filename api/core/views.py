from rest_framework import generics, pagination, permissions
from rest_framework.response import Response

from core.models import MyUser
from core.serializers import CurrentUsersSerializer, UsersSerializer

from rest_framework import status


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
    serializer_class = CurrentUsersSerializer
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
