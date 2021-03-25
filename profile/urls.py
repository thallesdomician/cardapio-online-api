from django.urls import path, reverse
from .views import ProfileCreate, ProfileUpdate, ProfileDetail

urlpatterns = [
    path('<int:pk>/update', ProfileUpdate.as_view(), name='profile_update'),
    path('<int:pk>', ProfileDetail.as_view(), name='profile_detail'),
    # path('sign-up', ProfileCreate.as_view(), name='register'),
]
