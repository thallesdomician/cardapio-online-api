"""cardapioOnlineApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

from plan.api.viewsets import PlanViewSet
from profile.views import LoginProfileView, UserCreate, CurrentUserView
from store.api.viewsets import StoreViewSet
from address.api.viewsets import AddressViewSet
from specialty.api.viewsets import SpecialtyViewSet
from profile.api.viewsets import ProfileViewSet
from profile import urls as profile_urls

# TODO implementar api version v1,v2,v3, etc... será que vale a pena?
#  https://www.django-rest-framework.org/api-guide/versioning/

router = routers.DefaultRouter()
router.register('store', StoreViewSet)
router.register('address', AddressViewSet)
router.register('specialty', SpecialtyViewSet)
router.register('plan', PlanViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
                  path('api/v1/', include(router.urls)),
                  path('admin/', admin.site.urls),
                  path('login/', LoginProfileView.as_view(), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('account', CurrentUserView.as_view()),
                  path('account/register', UserCreate.as_view()),

                  path('auth/', obtain_auth_token)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
