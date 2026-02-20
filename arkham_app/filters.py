from django_filters import rest_framework as filters
from .models import InmateProfile

class InmateProfileFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    cell_block = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = InmateProfile
        fields = ['name', 'cell_block']