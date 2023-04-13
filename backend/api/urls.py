from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductByYearViewSet, StateByYearViewSet, EvoState, EvoProduct

product = DefaultRouter()
product.register(r'product-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', ProductByYearViewSet, basename= 'product-year')

state = DefaultRouter()
state.register(r'state-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', StateByYearViewSet, basename= 'state-year')

# evoState = DefaultRouter()
# evoState.register(r'states-evo/<str:states>/', EvoState, basename='evo-state')
evoState_router = DefaultRouter()
evoState_router.register(r'', EvoState, basename='evo-state')

evoProduct = DefaultRouter()
evoProduct.register(r'product-evo/(?P<product>([A-Z]{2},)*[A-Z]{2})/', EvoState, basename= 'evo-product')

urlpatterns = [
    path('', include(product.urls)),
    path('', include(state.urls)),
    # path('', include(evoState.urls)),
    path('states-evo/<str:states>/', include(evoState_router.urls)),
    path('', include(evoProduct.urls))

]

