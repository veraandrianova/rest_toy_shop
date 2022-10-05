from django.urls import path

from .views import CreateReview, AddStarRatingProduct, CategoryView, ProductViewSet, CategoryDetailView

urlpatterns = [
    path('products/', ProductViewSet.as_view({'get': 'list'})),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'})),
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
    path('review/', CreateReview.as_view({'get': 'list', 'post': 'create'})),
    path('review/<int:pk>', CreateReview.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('rating/', AddStarRatingProduct.as_view({'post': 'create'})),
]
