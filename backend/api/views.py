from api.models import Files,OrderItem
from django.db.models import Count, F, Sum
# API
from rest_framework import generics
from api.serializers import CaStateSerializer, FilesSerializer, SoldProductSerializer, EvoStateSerializer, EvoProduitSerializer
from rest_framework.response import Response
from rest_framework import viewsets

class FilesList(generics.ListCreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer


##
# Vente d'un produit pour une années données
# EndPoint ->    http://localhost:8000/api/product-year/
#          ->    http://localhost:8000/api/product-year/<year>/<limit>
#          ->    http://localhost:8000/api/product-year//<limit>
#          ->    http://localhost:8000/api/product-year/<year>/
#
class ProductByYearViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SoldProductSerializer
    queryset = OrderItem.objects.none()  # an empty queryset

    def list(self, request, year, limit=None):

        sales_by_prod = OrderItem.objects\
            .filter(order__order_purchase_timestamp__year=year)\
            .values('product_id__product_id')\
            .annotate(product_id=F('product_id__product_id'),quantity=Sum('order_item_quantity'),turnover=Sum(F('price')*F('order_item_quantity')))\
            .values('product_id','quantity','turnover')\
            .order_by('-turnover')
        
        # Verifie si limit n'est pas null et qu'il est supèrieur a 0
        if limit is not None and limit.isdigit() and int(limit) > 0:
            sales_by_prod = sales_by_prod[:int(limit)]
        
        for item in sales_by_prod:
            print(item)

        
        serializer = self.serializer_class(sales_by_prod, many=True)
        return Response(serializer.data)
    
##
# Chiffre d'Affaire par Region et Quantité de produit vendu par region
# EndPoint -> http://localhost:8000/api/state-year/<year>/<limit> limit non obligatoire
#
class StateByYearViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CaStateSerializer
    queryset = OrderItem.objects.none()  # an empty queryset

    def list(self, request, year, limit=None):

        sales_by_state = OrderItem.objects\
            .filter(order__order_purchase_timestamp__year=year)\
            .values('seller_id__city_id__state__state_name')\
            .annotate(state_name=F('seller_id__city_id__state__state_name'),quantity=Sum('order_item_quantity'),turnover=Sum(F('price')*F('order_item_quantity')))\
            .values('state_name','quantity','turnover')\
            .order_by('-turnover')
        
        # Verifie si limit n'est pas null et qu'il est supèrieur a 0
        if limit is not None and limit.isdigit() and int(limit) > 0:
            sales_by_state = sales_by_state[:int(limit)]
        
        for item in sales_by_state:
            print(item)

        
        serializer = self.serializer_class(sales_by_state, many=True)
        return Response(serializer.data)

##
# Renvoye l'evolution des region passé en paramettre
# EndPoint -> http://localhost:8000/api/evo-state/<state>/ |ex| http://localhost:8000/api/evo-state/<1>,<2>,<3>/
#
class EvoState(viewsets.ReadOnlyModelViewSet):
    serializer_class = EvoStateSerializer
    queryset = OrderItem.objects.none()  # an empty queryset

    def list(self, request, states):
        state_list = states.split(',')
        print(state_list)
        evo_state = OrderItem.objects\
            .filter(seller__city__state__state_name__in=state_list)\
            .values('seller_id__city_id__state__state_name','order__order_purchase_timestamp__year')\
            .annotate(state_name=F('seller_id__city_id__state__state_name'),year=F('order__order_purchase_timestamp__year'),quantity=Count('order_item_quantity'),turnover=Sum(F('price')*F('order_item_quantity')))\
            .order_by('seller__city__state__state_name', 'order__order_purchase_timestamp__year')
        
        state_dict = {}
        for item in evo_state:
            state_name = item['state_name']
            data = {
                'quantity': item['quantity'],
                'turnover': item['turnover'],
                'year': item['year'],
            }
            if state_name not in state_dict:
                state_dict[state_name] = {'state_name': state_name, 'data': [data]}
            else:
                state_dict[state_name]['data'].append(data)

        state_list = list(state_dict.values())

        serializer = self.serializer_class(state_list, many=True)
        return Response(serializer.data)
    

##
# Renvoye l'evolution des produits passé en paramettre
# EndPoint -> http://localhost:8000/api/evo-product/<produit>/ |ex| http://localhost:8000/api/evo-product/<1>,<2>,<3>/
#
class EvoProduct(viewsets.ReadOnlyModelViewSet):

    serializer_class = EvoProduitSerializer

    # def list(self, request, product):
    #     evo_product = OrderItem.objects\
    #     .filter(order__product__product_id=product)\
    #     .values('order__product__product_id','order__order_purchase_timestamp__year')\
    #     .annotate(quantity=Count('order_item_quantity'),turnover=Count(F('price')*F('order_item_quantity')))\
    #     .order_by('order__product__product_id')
        
    #     serializer = self.serializer_class(evo_product, many=True)
    #     return Response(serializer.data)
    






            # if year is None and limit is None:
        #     sales_by_state = OrderItem.objects\
        #         .values('order__order_item__sellers__city__state__state_id__state_name')\
        #         .annotate(quantity=Count('order_item_quantity'),turnover=Count(F('price')*F('order_item_quantity')))\
        #         .order_by('-total')

        # # Cas ou Il n'y a que l'années
        # elif year is None:
        #     sales_by_state = OrderItem.objects\
        #         .values('order__order_item__sellers__city__state__state_id__state_name')\
        #         .annotate(quantity=Count('order_item_quantity'),turnover=Count(F('price')*F('order_item_quantity')))\
        #         .order_by('-total')[:limit]

        # # Cas ou Il n'y a que la limite
        # elif limit is None:
        #     sales_by_state = OrderItem.objects\
        #         .filter(order__order_purchase_timestamp__year=year)\
        #         .values('order__order_item__sellers__city__state__state_id__state_name')\
        #         .annotate(quantity=Count('order_item_quantity'),turnover=Count(F('price')*F('order_item_quantity')))\
        #         .order_by('-total')

        # # Cas ou il y a les deux parametres
        # else: