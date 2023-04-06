from api.models import Files,OrderItem
from django.db.models import Count, F
# API
from rest_framework import generics
from api.serializers import CaStateSerializer, FilesSerializer, SoldProductSerializer, EvoStateSerializer
from rest_framework.response import Response
from rest_framework import viewsets

class FilesList(generics.ListCreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer


##
# Vente d'un produit pour une années données
# EndPoint ->    http://localhost:8000/api/colonne/product-year/
#          ->    http://localhost:8000/api/colonne/product-year/<year>/<limit>
#          ->    http://localhost:8000/api/colonne/product-year//<limit>
#          ->    http://localhost:8000/api/colonne/product-year/<year>/
#
class ProductByYearViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SoldProductSerializer

    def list(self, request, year, limit):

        # Cas ou aucun parametre est entré
        if year is None and limit is None:
            sales_by_product = OrderItem.objects\
                .values('product__product_id')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')

        # Cas ou Il n'y a que l'années
        elif year is None:
            sales_by_product = OrderItem.objects\
                .values('product__product_id')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')[:limit]

        # Cas ou Il n'y a que la limite
        elif limit is None:
            sales_by_product = OrderItem.objects\
                .filter(order__order_purchase_timestamp__year=year)\
                .values('product__product_id')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')

        # Cas ou il y a les deux parametres
        else:
            sales_by_product = OrderItem.objects\
                .filter(order__order_purchase_timestamp__year=year)\
                .values('product__product_id')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')[:limit]    


        serializer = self.serializer_class(sales_by_product, many=True)
        return Response(serializer.data)
    
##
# Chiffre d'Affaire par Region et Quantité de produit vendu par region
# EndPoint -> http://localhost:8000/api/colonne/state-year/<year>/
#
class StateByYearViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CaStateSerializer

    def list(self, request, year, limit):

        if year is None and limit is None:
            sales_by_state = OrderItem.objects\
                .values('order__order_intem__sellers__geolocation__state__state_id__state_name')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')

        # Cas ou Il n'y a que l'années
        elif year is None:
            sales_by_state = OrderItem.objects\
                .values('order__order_intem__sellers__geolocation__state__state_id__state_name')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')[:limit]

        # Cas ou Il n'y a que la limite
        elif limit is None:
            sales_by_state = OrderItem.objects\
                .filter(order__order_purchase_timestamp__year=year)\
                .values('order__order_intem__sellers__geolocation__state__state_id__state_name')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')

        # Cas ou il y a les deux parametres
        else:
            sales_by_state = OrderItem.objects\
                .filter(order__order_purchase_timestamp__year=year)\
                .values('order__order_intem__sellers__geolocation__state__state_id__state_name')\
                .annotate(quantity=Count('order_item_quantity'),total=Count(F('price')*F('order_item_quantity')))\
                .order_by('-total')[:limit]

        
        serializer = self.serializer_class(sales_by_state, many=True)
        return Response(serializer.data)



class TopEvoState(viewsets.ReadOnlyModelViewSet):
    serializer_class = EvoStateSerializer

    def list(self, request, states):
        evo_state = OrderItem.objects\
            .values('order__order_purchase_timestamp__year','order__order_intem__sellers__geolocation__state__state_id__state_name')\
            .annotate(total=Count(F('price')*F('order_item_quantity')))\
            .order_by('order__order_intem__sellers__geolocation__state__state_id__state_name')
        
        serializer = self.serializer_class(evo_state, many=True)
        return Response(serializer.data)