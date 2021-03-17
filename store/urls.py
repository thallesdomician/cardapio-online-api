from rest_framework import routers

router = routers.SimpleRouter()
router.register('accounts/{slug}/category', StoreCategoryViewSet)
urlpatterns = router.urls