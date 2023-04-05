from api.models import Files,OrderItem
from django.db.models import Count, F
# API
from rest_framework import generics
from api.serializers import FilesSerializer, GeolocationNormSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework import viewsets

class FilesList(generics.ListCreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer


##
# Vente d'un produit pour une années données
# EndPoint -> http://localhost:8000/api/colonne/product-year/<year>/
#
class ProductByYearViewSet(viewsets.ViewSet):
    serializer_class = OrderItemSerializer

    def list(self, request, year):
        sales_by_product = OrderItem.objects\
            .filter(order__order_purchase_timestamp__year=year)\
            .values('product__product_id')\
            .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
            .order_by('-sales')
        serializer = self.serializer_class(sales_by_product, many=True)
        return Response(serializer.data)
    

class StateByYearViewSet(viewsets.ViewSet):
    serializer_class = GeolocationNormSerializer

    def list(self, request, year):
        sales_by_state = OrderItem.objects\
            .filter(order__order_purchase_timestamp__year=year)\
            .values('order__order_intem__sellers__geolocation_zip_code_prefix__geolocation_state')\
            .annotate()
        




    #     class SalesByProductYearByState(APIView):
    # def get(self, request, year):
    #     sales_by_state = OrderItem.objects\
    #         .filter(order__order_purchase_timestamp__year=year)\
    #         .values('product__product_id', 'product__product_category_name', 'order__customer__geolocation_zip_code_prefix__geolocation_state')\
    #         .annotate(sales=Count('order_item_quantity'))\
    #         .order_by('order__customer__geolocation_zip_code_prefix__geolocation_state')
    #     return Response(sales_by_state)