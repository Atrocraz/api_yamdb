from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .permissions import IsAdmin
from .serializers import UserCodeSerializer, UserJWTSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_confirmation_code(request):
    '''API-view функция регистрации пользователя.

    Ожидает на вход поля username и email.
    В качестве ответа на запрос возвращает поля username и email.
    Отправляет пользователю код подтверждения на почту и
    Сохраняет его в базу данных для последующей сверки.
    '''
    user = CustomUser.objects.filter(username=request.data.get('username'),
                                     email=request.data.get('email'))
    if user.first():
        serializer = UserCodeSerializer(user.first(), data=request.data)
        resp_status = status.HTTP_200_OK
    else:
        serializer = UserCodeSerializer(data=request.data)
        resp_status = status.HTTP_200_OK

    if serializer.is_valid():
        send_conf_code(serializer.validated_data.get('email'),
                       serializer.validated_data.get('confirmation_code'))
        serializer.save()
        return Response(serializer.data, status=resp_status)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    '''API-view функция отправки JWT-кода.

    Ожидает на вход поля username и confirmation_code.
    В качестве ответа на запрос возвращает JWT-токен.
    '''
    serializer = UserJWTSerializer(data=request.data)
    if serializer.is_valid():
        user = CustomUser.objects.filter(username=request.data.get('username'))
        refresh = RefreshToken.for_user(user.first())
        response_data = {'token': str(refresh.access_token)}
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    '''API-viewset класс для обработки запросов по модели пользователя.

    Обрабатывает следующие эндпоинты:
    /users/
    /users/{username}/
    /users/me/
    '''
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False,
            methods=['GET', 'PATCH'],
            url_path='me',
            permission_classes=[IsAuthenticated])
    def user_profile(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        context={'action': 'patchme'},
                                        partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_conf_code(email, conf_code):
    "Функция-шорткат для отправки письма."
    send_mail(
        subject='[YaMDB] Код подтверждения',
        message=('Добрый день!\n'
                 f'Ваш код подтверждения - {conf_code}'),
        from_email='from@example.com',
        recipient_list=[email],
        fail_silently=True,
    )
