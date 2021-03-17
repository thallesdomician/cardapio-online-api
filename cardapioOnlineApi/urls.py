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

from product.api.viewset import CategoryViewSet
from profile.api.viewsets import ProfileViewSet
from plan.api.viewsets import PlanViewSet
from store.api.viewsets import StoreViewSet
from address.api.viewsets import AddressViewSet
from specialty.api.viewsets import SpecialtyViewSet

# TODO implementar api version v1,v2,v3, etc... será que vale a pena?
#  https://www.django-rest-framework.org/api-guide/versioning/

router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('store', StoreViewSet)
router.register('address', AddressViewSet)
router.register('specialty', SpecialtyViewSet)
router.register('plan', PlanViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('auth.urls')),
                  path('api/', include(router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


