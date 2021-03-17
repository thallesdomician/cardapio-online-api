from rest_framework.decorators import action
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product.api.serializer import CategorySerializer
from product.models import Category
from store.api.viewsets import StandardResultsSetPagination
from store.models import Store

from rest_framework import viewsets, mixins


class CategorySampleViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    pass


class CategoryViewSet(CategorySampleViewSet):
    queryset = Category.objects.filter(deleted_at__isnull=True, store__deleted_at__isnull=True)
    pagination_class = StandardResultsSetPagination

    serializer_class = CategorySerializer

    filter_fields = ('id', 'name', 'store')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            store = Store.objects.get(pk=request.data['store'], deleted_at__isnull=True)
        except Store.DoesNotExist:
            raise Http404
        user = request.user
        if not user.has_perm('store.change_store', store):
            raise PermissionDenied({"message": "You don't have permission to create",
                                    "object_id": store.id})

        self.perform_create(serializer)
        return super(CategoryViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if not user.has_perm('store.change_store', instance.store):
            raise PermissionDenied({"message": "You don't have permission to delete",
                                    "object_id": instance.id})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
