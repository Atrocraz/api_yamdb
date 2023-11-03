import users.views as views
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', views.get_jwt_token),
    path('v1/auth/signup/', views.obtain_confirmation_code),
    path('v1/', include(router_v1.urls)),
]
