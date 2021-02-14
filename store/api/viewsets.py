from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.api.serializers import StoreSerializer
from store.models import Store

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    pagination_class = StandardResultsSetPagination

    serializer_class = StoreSerializer

    filter_fields = ('name', 'specialty')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super(StoreViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        kwargs['pk']
        pass
