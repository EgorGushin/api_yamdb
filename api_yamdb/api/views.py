from rest_framework import filters

from categories.models import Category, Genre, Title

class CategoryViewSet():
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    permission_classes = 
    filter_backend = (filters.SearchFilter)
    search_fields = ('name',)
