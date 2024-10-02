import django_filters
from app import models
from django.db.models import Q

# class UnitFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(lookup_expr='icontains')
#     class Meta:
#         model = models.Unit
#         fields = ['name']

class InventoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search')

    class Meta:
        model = models.Inventory
        fields = []

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |  
            Q(quantity__icontains=value)
        )

class RecipeFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr = 'icontains')
    class Meta:
        model = models.Recipe
        fields = ['name']
        
