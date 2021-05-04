from django.urls import path
from .views import ProfileUpdate, ProfileDetail

urlpatterns = [
    path('<int:pk>/update', ProfileUpdate.as_view(), name='profile_update'),
    path('<int:pk>', ProfileDetail.as_view(), name='profile_detail'),
    # path('sign-up', ProfileCreate.as_view(), name='register'),
]
