from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductByYearViewSet, StateByYearViewSet, EvoState, EvoProduct, importCsv

product = DefaultRouter()
product.register(r'product-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', ProductByYearViewSet, basename= 'product-year')

state = DefaultRouter()
state.register(r'state-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', StateByYearViewSet, basename= 'state-year')

evoState = DefaultRouter()
evoState.register(r'', EvoState, basename='evo-state')

evoProduct = DefaultRouter()
evoProduct.register(r'', EvoProduct, basename= 'evo-product')

urlpatterns = [
    path('', include(product.urls)),
    path('', include(state.urls)),
    path('states-evo/<str:states>/', include(evoState.urls)),
    path('product-evo/<str:product>/', include(evoProduct.urls)),
    path('import', importCsv, name="importcsv"),


]

