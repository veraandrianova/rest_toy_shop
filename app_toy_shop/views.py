from django.db import models
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Review, Category
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthOrReadOnly
from .serializers import ProductListSerializers, ProductDetailSerializers, CreateReviewSerializers, \
    CreateRatingSerializer, CategorySerializers, ProductCreateSerializers
from .service import get_client_ip, PaginatorProduct, ProductFilter, get_url


# Create your views here.
class ProductsViewSet(viewsets.ModelViewSet):
    '''Вывод всех продуктов'''
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsOwnerOrReadOnly, IsAdminOrReadOnly)
    pagination_class = PaginatorProduct
    filterset_class = ProductFilter
    permission_classes_by_action = {'list': [IsAuthenticatedOrReadOnly],
                                    'retrieve': [IsAuthenticatedOrReadOnly]}
    serializer_classes_by_action = {
        'list': ProductListSerializers,
        'update': ProductCreateSerializers,
        'destroy': ProductCreateSerializers,
        'create': ProductCreateSerializers,
        'retrieve': ProductDetailSerializers
    }

    def get_queryset(self):
        products = Product.objects.filter(is_active=True).annotate(
            rating_user=models.Count('product_star', filter=models.Q(product_star__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('product_star__star')) / models.Count(models.F('product_star'))
        )
        return products

    def perform_create(self, serializer):
        serializer.save(url=get_url(self.request))

    def perform_update(self, serializer):
        serializer.save(url=get_url(self.request))


    def get_serializer(self, *args, **kwargs):
        try:
            serializer_class = self.serializer_classes_by_action[self.action]
        except KeyError:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)



# class ProductViewSet(viewsets.ModelViewSet):
#     '''Вывод одного продуктов'''
#     filter_backends = (DjangoFilterBackend,)
#     serializer_class = ProductCreateSerializers
#     permission_classes = (IsOwnerOrReadOnly, IsAdminOrReadOnly)
#     pagination_class = PaginatorProduct
#     filterset_class = ProductFilter
#
#     def get_queryset(self):
#         products = Product.objects.filter(is_active=True).annotate(
#             rating_user=models.Count('product_star', filter=models.Q(product_star__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('product_star__star')) / models.Count(models.F('product_star'))
#         )
#         return products
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return ProductDetailSerializers
#         elif self.action == 'update' or self.action == 'destroy':
#             return ProductCreateSerializers
#
#     def perform_update(self, serializer):
#         serializer.save(url=get_url(self.request))


# class ProductListView(generics.ListAPIView):
#     '''Вывод всех продуктов'''
#
#     serializer_class = ProductListSerializers
#     filter_backends = (DjangoFilterBackend, )
#
#     def get_queryset(self):
#         products = Product.objects.filter(is_active=True).annotate(
#             rating_user=models.Count('product_star', filter=models.Q(product_star__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('product_star__star')) / models.Count(models.F('product_star'))
#         )
#         return products


# class ProductDetailView(APIView):
#     '''Детали одного продукта'''
#
#     def get(self, request, pk):
#         product = Product.objects.get(id=pk, is_active=True)
#         serializer = ProductDetailSerializers(product)
#         return Response(serializer.data)

# class ProductDetailView(generics.RetrieveAPIView):
#     '''Детали одного продукта'''
#
#     queryset = Product.objects.filter(is_active=True)
#     serializer_class = ProductDetailSerializers


class CreateReview(viewsets.ModelViewSet):
    '''Добавление отзыва'''
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializers

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]


# class AddStarRatingProduct(APIView):
#     '''Добавление звезд рейтинга'''
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=200)
#         else:
#             return Response(status=400)

# class AddStarRatingProduct(generics.CreateAPIView):
#     '''Добавление звезд рейтинга'''
#
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))


class AddStarRatingProduct(viewsets.ModelViewSet):
    '''Добавление звезд рейтинга'''

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class CategoryView(viewsets.ModelViewSet):
    '''Категории'''

    queryset = Category.objects.all()
    serializer_class = CategorySerializers


# class CategoryDetailView(generics.RetrieveAPIView):
#     '''Детали одной категории'''
#
#     queryset = Category.objects.filter()
#     serializer_class = CategorySerializers
