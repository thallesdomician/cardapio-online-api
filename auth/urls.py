from django.urls import path, include
from auth.views import RegisterOwnerView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('register/', RegisterOwnerView.as_view(), name='auth_register'),
    path('login/', obtain_jwt_token),
    path('api-auth/', include('rest_framework.urls')),
]
