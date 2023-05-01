from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProductByYearViewSet, StateByYearViewSet, EvoState, EvoProduct, TurnoverYear, NewCustomerYear , InterVsExter, importCsv

product = DefaultRouter()
product.register(r'product-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', ProductByYearViewSet, basename= 'product-year')

state = DefaultRouter()
state.register(r'state-year/(?:(?P<year>\d{4})(?:/(?P<limit>\d{1}))?)?', StateByYearViewSet, basename= 'state-year')

evoState = DefaultRouter()
evoState.register(r'', EvoState, basename='evo-state')

turnoverYear = DefaultRouter()
turnoverYear.register(r'customers-year/(?:(?P<year>\d{4}))?', NewCustomerYear, basename='customers-year')

newCustomers = DefaultRouter()
newCustomers.register(r'turnover-year/(?:(?P<year>\d{4}))?', TurnoverYear, basename='turnover-year')

interExter = DefaultRouter()
interExter.register(r'inter-exter/(?:(?P<year>\d{4}))?', InterVsExter, basename='inter-exter')

evoProduct = DefaultRouter()
evoProduct.register(r'', EvoProduct, basename= 'evo-product')

urlpatterns = [
    path('', include(product.urls)),
    path('', include(state.urls)),
    path('', include(turnoverYear.urls)),
    path('', include(newCustomers.urls)),
    path('', include(interExter.urls)),
    path('states-evo/<str:states>/', include(evoState.urls)),
    path('product-evo/<str:product>/', include(evoProduct.urls)),
    path('import', importCsv, name="importcsv"),


]

