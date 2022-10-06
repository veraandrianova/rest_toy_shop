from django.db import models
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Review, Category
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import ProductListSerializers, ProductDetailSerializers, CreateReviewSerializers, \
    CreateRatingSerializer, CategorySerializers
from .service import get_client_ip, PaginatorProduct, ProductFilter


# Create your views here.
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вывод продуктов'''
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsOwnerOrReadOnly, IsAdminOrReadOnly)
    pagination_class = PaginatorProduct
    filterset_class = ProductFilter

    def get_queryset(self):
        products = Product.objects.filter(is_active=True).annotate(
            rating_user=models.Count('product_star', filter=models.Q(product_star__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('product_star__star')) / models.Count(models.F('product_star'))
        )
        return products

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializers
        elif self.action == 'retrieve':
            return ProductDetailSerializers


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
    permission_classes = (IsAuthenticated, )

    # def post(self, request):
    #     review = CreateReviewSerializers(data=request.data)
    #     if review.is_valid():
    #         review.save()
    #     return Response(status=200)


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

class CategoryView(generics.ListAPIView):
    '''Категории'''

    queryset = Category.objects.all()
    serializer_class = CategorySerializers

class CategoryDetailView(generics.RetrieveAPIView):
    '''Детали одной категории'''

    queryset = Category.objects.filter()
    serializer_class = CategorySerializers

