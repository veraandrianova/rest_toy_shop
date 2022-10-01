from django.urls import path

from .views import CreateReview, AddStarRatingProduct, Category, ProductViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view({'get': 'list'})),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'})),
    path('review/', CreateReview.as_view({'get': 'list', 'post': 'create'})),
    path('review/<int:pk>', CreateReview.as_view({'get': 'retrieve'})),
    path('rating/', AddStarRatingProduct.as_view({'post': 'create'})),
    path('category/', Category.as_view())
]
