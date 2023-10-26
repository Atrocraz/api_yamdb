from django.urls import path

import users.views as views

urlpatterns = [
    path('v1/auth/signup/', views.obtain_confirmation_code),
    path('v1/auth/token/', views.get_jwt_token),
]
