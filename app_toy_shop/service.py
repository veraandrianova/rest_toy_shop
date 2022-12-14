from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from transliterate import translit



from .models import Product

class PaginatorProduct(PageNumberPagination):
    page_size = 1
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


def get_client_ip(request):
    '''Получение ip пользователя'''

    x = request.META.get('HTTP_X_FORWARDED_FOR')
    if x:
        ip = x.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_url(request):
    '''Получение url продукта'''

    cur_url = request.data.get('name').lower().replace(' ', '_')
    url = translit(cur_url, language_code='ru', reversed=True)
    return url

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()
    category = CharFilterInFilter(field_name='category__name', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['category', 'price']
