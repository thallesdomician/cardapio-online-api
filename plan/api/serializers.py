from rest_framework.serializers import ModelSerializer

from plan.models import Plan


class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'name', 'active', 'description', 'price', 'created_at', 'updated_at')
