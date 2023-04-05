from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductByYearViewSet

product = DefaultRouter()
product.register(r'product-year/(?P<year>\d{4})', ProductByYearViewSet, basename= 'product-year')

urlpatterns = [
    path('', include(product.urls)),

]