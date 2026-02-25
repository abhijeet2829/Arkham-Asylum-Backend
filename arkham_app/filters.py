from django_filters import rest_framework as filters
from .models import InmateProfile

class InmateProfileFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    cell_block = filters.CharFilter(field_name='cell_block__name', lookup_expr='iexact')

    class Meta:
        model = InmateProfile
        fields = ['name', 'cell_block']