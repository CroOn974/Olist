from api.models import Files,OrderItem,State,City,Sellers
from django.db.models import Count, F, Sum
import pandas as pd
# API
from rest_framework import generics
from api.serializers import CaStateSerializer, FilesSerializer, SoldProductSerializer, EvoStateSerializer, EvoProductSerializer
from rest_framework.response import Response
from django.http import JsonResponse
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

    serializer_class = EvoProductSerializer
    queryset = OrderItem.objects.none()  # an empty queryset

    def list(self, request, product):
        product_list = product.split(',')
        print(product_list)
        evo_product = OrderItem.objects\
            .filter(product__product_id__in=product_list) \
            .values('product_id__product_id','order__order_purchase_timestamp__year')\
            .annotate(product=F('product_id__product_id'),year=F('order__order_purchase_timestamp__year'),quantity=Count('order_item_quantity'),turnover=Sum(F('price')*F('order_item_quantity')))\
            .order_by('product_id__product_id', 'order__order_purchase_timestamp__year')
        
        for item in evo_product:
            print(item)


        product_dict = {}
        for item in evo_product:
            print(item)
            product = item['product']
            data = {
                'quantity': item['quantity'],
                'turnover': item['turnover'],
                'year': item['year'],
            }
            if product not in product_dict:
                product_dict[product] = {'product': product, 'data': [data]}
            else:
                product_dict[product]['data'].append(data)

        product_list = list(product_dict.values())

        serializer = self.serializer_class(product_list, many=True)
        return Response(serializer.data)


##
# Upload Fichier csv
#
#

def importCsv (request):

    # insertState()
    # insertCity()
    # insertSellers()

    data = {'message': 'Hello, World!'}
    return JsonResponse(data, content_type='application/json')

def insertState():

    geo_directory = 'api/upload/olist_geolocation_dataset_propre.csv'
    geo_file = pd.read_csv(geo_directory, encoding='unicode_escape')
    new_geolocation_state = geo_file['geolocation_state'].drop_duplicates()

    exist_geolocation_state = pd.DataFrame(list(State.objects.all().values()))

    # On ne peut pas concat un dataframe vide
    if exist_geolocation_state.empty:
        geolocation_state = new_geolocation_state
    else:
        geolocation_state = pd.concat([exist_geolocation_state,new_geolocation_state,exist_geolocation_state]).drop_duplicates(subset=['state_name'],keep=False)

    if geolocation_state.empty == False:
        state_objects = [State(state_name=state_name) for state_name in geolocation_state]
        State.objects.bulk_create(state_objects)
   

def insertCity():
    geo_directory = 'api/upload/olist_geolocation_dataset_propre.csv'
    geo_file = pd.read_csv(geo_directory, encoding='unicode_escape')

    geo_state = pd.DataFrame(list(State.objects.all().values()))
    geo_city = geo_file[['geolocation_city', 'geolocation_state']].drop_duplicates(subset=['geolocation_city'],keep='first')

    print(geo_city)

    # Fusionner les deux DataFrames
    merged_geo_city = pd.merge(geo_state, geo_city, left_on='state_name', right_on='geolocation_state')
    merged_geo_city = merged_geo_city[['state_id','geolocation_city']]

    exist_city = pd.DataFrame(list(City.objects.all().values()))
    
    if exist_city.empty:
        city = merged_geo_city
    else:
        city = pd.concat([exist_city,merged_geo_city,exist_city]).drop_duplicates(subset=['state_name'],keep=False)

    if city.empty == False:
        city['city_object'] = city.apply(lambda row: City(city_name=row['geolocation_city'], state_id=row['state_id']), axis=1)
        city_objects = city['city_object'].tolist()
        City.objects.bulk_create(city_objects)


def insertSellers():
    seller_directory = 'api/upload/olist_sellers_dataset_propre.csv'
    seller_file = pd.read_csv(seller_directory, encoding='unicode_escape')
    seller =  seller_file[['seller_id','seller_city']]
    print(seller)

    geo_city = pd.DataFrame(list(City.objects.all().values()))
    exist_sellers = pd.DataFrame(list(Sellers.objects.all().values()))

    # Fusionner les deux DataFrames
    merged_seller_city = pd.merge(seller, geo_city, left_on='seller_city', right_on='city_name')
    seller_city = merged_seller_city[['seller_id','city_id']]
    
    if exist_sellers.empty:
        sellers = seller_city
    else:
        sellers = pd.concat([exist_sellers,seller_city,exist_sellers]).drop_duplicates(subset=['state_name'],keep=False)

    if not sellers.empty:
        sellers['seller_object'] = sellers.apply(lambda row: Sellers(seller_id=row['seller_id'], city_id=row['city_id']), axis=1)
        sellers_objects = sellers['seller_object'].tolist()
        Sellers.objects.bulk_create(sellers_objects)