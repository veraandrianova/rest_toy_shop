from django_filters import rest_framework as filters

# from rest_toy_shop.app_toy_shop.models import Product


def get_client_ip(request):
    '''Получение ip пользователя'''

    x = request.META.get('HTTP_X_FORWARDED_FOR')
    if x:
        ip = x.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass
#
#
# class ProductFilter(filters.FilterSet):
#     price = filters.RangeFilter()
#     category = CharFilterInFilter(field_name='category__name', lookup_expr='in')
#
#     class Meta:
#         model = Product
#         fields = ['category', 'price']