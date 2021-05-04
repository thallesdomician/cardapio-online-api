from rest_framework.viewsets import ModelViewSet

from plan.api.serializers import PlanSerializer
from plan.models import Plan


class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.all()

    serializer_class = PlanSerializer
