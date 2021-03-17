from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from product.models import Category
from store.api.serializers import StoreSerializer, StoreCategorySerializer
from store.models import Store

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.filter(deleted_at__isnull=True)
    pagination_class = StandardResultsSetPagination

    serializer_class = StoreSerializer

    filter_fields = ('name', 'specialty')

    lookup_field = 'slug'

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
        queryset = Category.objects.filter(deleted_at__isnull=True, store=store)


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = StoreCategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StoreCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super(StoreViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if not user.has_perm('store.delete_store', instance):
            raise PermissionDenied({"message": "You don't have permission to delete",
                                    "object_id": instance.id})

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
