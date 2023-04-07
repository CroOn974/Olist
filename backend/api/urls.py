from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductByYearViewSet, StateByYearViewSet, EvoState, EvoProduct

product = DefaultRouter()
product.register(r'product-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', ProductByYearViewSet, basename= 'product-year')

state = DefaultRouter()
state.register(r'state-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', StateByYearViewSet, basename= 'state-year')

evoState = DefaultRouter()
evoState.register(r'state-evo/(?P<state>([A-Z]{2},)*[A-Z]{2})/', EvoState, basename= 'evo-state')

evoProduct = DefaultRouter()
evoProduct.register(r'product-evo/(?P<product>([A-Z]{2},)*[A-Z]{2})/', EvoState, basename= 'evo-product')

urlpatterns = [
    path('', include(product.urls)),
    path('', include(state.urls)),
    path('', include(evoState.urls)),
    path('', include(evoProduct.urls))

]

