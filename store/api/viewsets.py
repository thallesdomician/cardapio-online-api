from django.core.files.base import ContentFile
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from product.models import Category
from store.api.serializers import StoreSerializer, StoreCategorySerializer, StoreLogoSerializer, StoreAvatarSerializer, \
    StoreWallpaperSerializer
from store.models import Store, StoreAvatar


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class StoreOwnerViewSet(ModelViewSet):
    queryset = Store.objects.filter(deleted_at__isnull=True)
    pagination_class = StandardResultsSetPagination

    serializer_class = StoreSerializer

    filter_fields = ('name', 'specialty')

    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        allowed = get_objects_for_user(user, ['store.change_store'])
        return Store.objects.filter(pk__in=allowed, deleted_at__isnull=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='category', url_name='store_category')
    def retrieve_categories(self, request, *args, **kwargs):
        store = self.get_object()
        user = request.user
        if not user.has_perm('store.change_store', store):
            raise PermissionDenied({"message"  : "You don't have permission to change",
                                    "object_id": store.id})
        queryset = Category.objects.filter(deleted_at__isnull=True, store=store)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = StoreCategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StoreCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super(StoreOwnerViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if not user.has_perm('store.delete_store', instance):
            raise PermissionDenied({"message"  : "You don't have permission to delete",
                                    "object_id": instance.id})

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def logo(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.retrieve_logo(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.change_logo(request, *args, **kwargs)

    def retrieve_logo(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StoreLogoSerializer(instance)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='avatar', url_name='store_avatar')
    def change_avatar(self, request, *args, **kwargs):
        store = self.get_object()
        user = request.user
        if not user.has_perm('store.change_store', store):
            raise PermissionDenied({"message"  : "You don't have permission to change",
                                    "object_id": store.id})
        serializer = StoreAvatarSerializer(data=request.data,  context={"request":request})

        if serializer.is_valid():
            if store.avatar:
                store.avatar.delete()
            avatar = serializer.create(serializer.validated_data)
            avatar.store = store
            avatar.save()
            serializer = StoreAvatarSerializer(avatar,  context={"request":request})

            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='wallpaper', url_name='store_wallpaper')
    def change_wallpaper(self, request, *args, **kwargs):
        store = self.get_object()
        user = request.user
        if not user.has_perm('store.change_store', store):
            raise PermissionDenied({"message"  : "You don't have permission to change",
                                    "object_id": store.id})
        serializer = StoreWallpaperSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            if store.wallpaper:
                store.wallpaper.delete()
            wallpaper = serializer.create(serializer.validated_data)
            wallpaper.store = store
            wallpaper.save()
            serializer = StoreWallpaperSerializer(wallpaper, context={"request": request})

            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
