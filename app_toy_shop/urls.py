from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CreateReview, AddStarRatingProduct, CategoryView, ProductsViewSet

product_list = ProductsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

product_detail = ProductsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

reviews = CreateReview.as_view({
    'get': 'list',
    'post': 'create'
})

detail_review = CreateReview.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

create_rating = AddStarRatingProduct.as_view({
    'post': 'create'
})

category_list = CategoryView.as_view({
    'get': 'list'
})

category_detail = CategoryView.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='products_detail'),
    path('category/', category_list, name='category_list'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('review/', reviews, name='reviews'),
    path('review/<int:pk>', detail_review, name='detail_review'),
    path('rating/', create_rating, name='create_rating'),
])
