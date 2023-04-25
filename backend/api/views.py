from api.models import Files,OrderItem,State,City,Sellers,Customers,OrderPlaced,Products,OrderItem,Payments,Reviews
from django.db.models import Count, F, Sum
import pandas as pd
import numpy as np
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

    insertState()
    insertCity()
    insertSellers()
    insertCustomers()
    insertOrder()
    insertProduct()
    insertOrderItem()
    insertOrderPayment()
    insertOrderReviews()

    data = {'message': 'Hello, World!'}
    return JsonResponse(data, content_type='application/json')

##
# Insert les region en bdd
#
def insertState():
    # récupère le csv
    geo_directory = 'api/upload/olist_geolocation_dataset_propre.csv'
    geo_file = pd.read_csv(geo_directory, encoding='unicode_escape')
    geolocation_state = geo_file['geolocation_state'].drop_duplicates()

    # récupère les données deja présente
    exist_geolocation_state = pd.DataFrame(list(State.objects.all().values()))
    
    # enleve les données deja presente en bdd du csv
    if not exist_geolocation_state.empty:
        geolocation_state = geolocation_state[~geolocation_state.isin(exist_geolocation_state['state_name'])]

    # si il reste des données les enregistres
    if not geolocation_state.empty:
        state_objects = [State(state_name=state_name) for state_name in geolocation_state]
        State.objects.bulk_create(state_objects)
   
##
# Insert les villes en bdd
#
def insertCity():
    # récupère le csv
    geo_directory = 'api/upload/olist_geolocation_dataset_propre.csv'
    geo_file = pd.read_csv(geo_directory, encoding='unicode_escape')
    geo_city = geo_file[['geolocation_city', 'geolocation_state']].drop_duplicates(subset=['geolocation_city'],keep='first')

    # récupère les données deja présente
    geo_state = pd.DataFrame(list(State.objects.all().values()))

    # Associe les ville a leur region
    merged_geo_city = pd.merge(geo_state, geo_city, left_on='state_name', right_on='geolocation_state')
    city = merged_geo_city[['state_id','geolocation_city']]

    exist_city = pd.DataFrame(list(City.objects.all().values()))

    # enleve les données deja presente en bdd du csv
    if not exist_city.empty:
       city = city[~city['geolocation_city'].isin(exist_city['city_name'])]

    # si il reste des données les enregistres
    if city.empty == False:
        city['city_object'] = city.apply(lambda row: City(city_name=row['geolocation_city'], state_id=row['state_id']), axis=1)
        city_objects = city['city_object'].tolist()
        City.objects.bulk_create(city_objects)

##
# Insert les sellers en bdd
#
def insertSellers():
    # récupère le csv
    seller_directory = 'api/upload/olist_sellers_dataset_propre.csv'
    seller_file = pd.read_csv(seller_directory, encoding='unicode_escape')
    seller =  seller_file[['seller_id','seller_city']]

    geo_city = pd.DataFrame(list(City.objects.all().values()))
    exist_sellers = pd.DataFrame(list(Sellers.objects.all().values()))

    # Associe les sellers a l'id de leur region
    merged_seller_city = pd.merge(seller, geo_city, left_on='seller_city', right_on='city_name')
    sellers = merged_seller_city[['seller_id','city_id']]

    if not exist_sellers.empty:
       sellers = sellers[~sellers['seller_id'].isin(exist_sellers['seller_id'])]

    if not sellers.empty:
        sellers['seller_object'] = sellers.apply(lambda row: Sellers(seller_id=row['seller_id'], city_id=row['city_id']), axis=1)
        sellers_objects = sellers['seller_object'].tolist()
        Sellers.objects.bulk_create(sellers_objects)

##
# Insert les customers en bdd
#
def insertCustomers():
    # récupère le csv
    customer_directory = 'api/upload/olist_customers_dataset_propre.csv'
    customer_file = pd.read_csv(customer_directory, encoding='unicode_escape')
    customers = customer_file[['customer_id','customer_unique_id','customer_city']]
    print(customers)

    geo_city = pd.DataFrame(list(City.objects.all().values()))
    exist_customers = pd.DataFrame(list(Customers.objects.all().values()))

    # Associe les customers a l'id de leur region
    merged_customers_city = pd.merge(customers, geo_city, left_on='customer_city', right_on='city_name')
    customers = merged_customers_city[['customer_id','customer_unique_id','city_id']]

    if not exist_customers.empty:
       customers = customers[~customers['customer_id'].isin(exist_customers['customer_id'])]

    if not customers.empty:
        customers['customer_object'] = customers.apply(lambda row: Customers(customer_id=row['customer_id'],customer_unique_id=row['customer_unique_id'],city_id=row['city_id']), axis=1)
        customers_objects = customers['customer_object'].tolist()
        Customers.objects.bulk_create(customers_objects)

##
# Insert les factures en bdd
#
def insertOrder():
    orderPlaced_directory = 'api/upload/olist_orders_dataset_propre.csv'
    orderPlaced = pd.read_csv(orderPlaced_directory, encoding='unicode_escape')
    
    exist_orderPlaced = pd.DataFrame(list(OrderPlaced.objects.all().values()))

    # Replace empty values with None
    orderPlaced = orderPlaced.replace('', np.nan).replace(np.nan, None)

    customers = pd.DataFrame(list(Customers.objects.all().values('customer_id')))

    # Ne garde que les order avec des customer_id deja existant
    orders = orderPlaced[orderPlaced['customer_id'].isin(customers['customer_id'])]

    if not exist_orderPlaced.empty:
       orders = orders[~orders['order_id'].isin(exist_orderPlaced['order_id'])]
       
    if not orders.empty:
        orders['order_object'] = orders.apply(lambda row: OrderPlaced(order_id=row['order_id'],
                                                                      customer_id=row['customer_id'],
                                                                      order_status=row['order_status'],
                                                                      order_purchase_timestamp=row['order_purchase_timestamp'],
                                                                      order_approved_at=row['order_approved_at'],
                                                                      order_delivered_carrier_date=row['order_delivered_carrier_date'],
                                                                      order_delivered_customer_date=row['order_delivered_customer_date'],
                                                                      order_estimated_delivery_date=row['order_estimated_delivery_date']), axis=1)
        orders_objects =  orders['order_object'].tolist()
        OrderPlaced.objects.bulk_create(orders_objects)

##
# Insert les produits en bdd
#
def insertProduct():
    product_directory = 'api/upload/olist_products_dataset_propre.csv'
    product_file = pd.read_csv(product_directory, encoding='unicode_escape')

    exist_product = pd.DataFrame(list(Products.objects.all().values()))

    products = product_file

    if not exist_product.empty:
       products = products[~products['product_id'].isin(exist_product['product_id'])]

    if not products.empty:

        products['product_object'] = products.apply(lambda row: Products(product_id=row['product_id'],
                                                                         product_category_name=row['product_category_name'],
                                                                         product_name_lenght=row['product_name_lenght'],
                                                                         product_description_lenght=row['product_description_lenght'],
                                                                         product_photos_qty=row['product_photos_qty'],
                                                                         product_weight_g=row['product_weight_g'],
                                                                         product_length_cm=row['product_length_cm'],
                                                                         product_height_cm=row['product_height_cm'],
                                                                         product_width_cm=row['product_width_cm']), axis=1)
        products_objects = products['product_object'].tolist()
        Products.objects.bulk_create(products_objects)

##
# Insert la detail de la facture en bdd
#
# def insertOrderItem():
#     orderItem_directory = 'api/upload/olist_order_items_dataset_propre.csv'
#     orderItem = pd.read_csv(orderItem_directory, encoding='unicode_escape')

#     sellers = pd.DataFrame(list(Sellers.objects.all().values('seller_id')))
#     products = pd.DataFrame(list(Products.objects.all().values('product_id')))
#     orders = pd.DataFrame(list(OrderPlaced.objects.all().values('order_id')))
#     exist_orderItem = pd.DataFrame(list(OrderItem.objects.all().values()))

#     orderItem = orderItem[orderItem['seller_id'].isin(sellers['seller_id'])]
#     orderItem = orderItem[orderItem['product_id'].isin(products['product_id'])]
#     orderItem = orderItem[orderItem['order_id'].isin(orders['order_id'])]


#     if not exist_orderItem.empty:
#        orderItem = orderItem[~orderItem[['order_id', 'product_id', 'seller_id']].isin(exist_orderItem[['order_id', 'product_id', 'seller_id']])]

#     if not orderItem.empty:
        
#         orderItem_objects = []
#         for _, row in orderItem.iterrows():
#             order_placed = OrderPlaced.objects.get(order_id=row['order_id'])
#             product = Products.objects.get(product_id=row['product_id'])
#             seller = Sellers.objects.get(seller_id=row['seller_id'])

#             orderItem_object = OrderItem(order=order_placed, product=product, seller=seller, 
#                                          shipping_limit_date=row['shipping_limit_date'], price=row['price'],
#                                          freight_value=row['freight_value'], order_item_quantity=row['order_item_quantity'])
#             orderItem_objects.append(orderItem_object)

#         OrderItem.objects.bulk_create(orderItem_objects)

##
# Insert la detail de la facture en bdd
#
def insertOrderItem():
    orderItem_directory = 'api/upload/olist_order_items_dataset_propre.csv'
    orderItem = pd.read_csv(orderItem_directory, encoding='unicode_escape')

    sellers = pd.DataFrame(list(Sellers.objects.all().values('seller_id')))
    products = pd.DataFrame(list(Products.objects.all().values('product_id')))
    orders = pd.DataFrame(list(OrderPlaced.objects.all().values('order_id')))
    exist_orderItem = pd.DataFrame(list(OrderItem.objects.all().values()))

    orderItem = orderItem[orderItem['seller_id'].isin(sellers['seller_id'])]
    orderItem = orderItem[orderItem['product_id'].isin(products['product_id'])]
    orderItem = orderItem[orderItem['order_id'].isin(orders['order_id'])]

    unique_cols = ['order_id', 'product_id', 'seller_id']
    orderItem = orderItem.drop_duplicates(subset=unique_cols)

    if not exist_orderItem.empty:
       existing_data = exist_orderItem[unique_cols].drop_duplicates()
       orderItem = orderItem.merge(existing_data, on=unique_cols, how='left', indicator=True)
       orderItem = orderItem[orderItem['_merge'] == 'left_only'].drop(columns='_merge')

    if not orderItem.empty: 
        orderItem_objects = []
        for _, row in orderItem.iterrows():
            order_placed = OrderPlaced.objects.get(order_id=row['order_id'])
            product = Products.objects.get(product_id=row['product_id'])
            seller = Sellers.objects.get(seller_id=row['seller_id'])

            orderItem_object = OrderItem(order=order_placed, product=product, seller=seller, 
                                         shipping_limit_date=row['shipping_limit_date'], price=row['price'],
                                         freight_value=row['freight_value'], order_item_quantity=row['order_item_quantity'])
            orderItem_objects.append(orderItem_object)

        OrderItem.objects.bulk_create(orderItem_objects)

##
# Insert le payments en bdd
#
def insertOrderPayment():
    payments_directory = 'api/upload/olist_order_payments_dataset_propre.csv'
    payments = pd.read_csv(payments_directory, encoding='unicode_escape')

    exist_payments = pd.DataFrame(list(Payments.objects.all().values()))

    order_placed = pd.DataFrame(list(OrderPlaced.objects.all().values('order_id')))
    payments = payments[payments['order_id'].isin(order_placed['order_id'])]

    if not exist_payments.empty:
       payments = payments[~payments['order_id'].isin(exist_payments['order_id'])]

    if not payments.empty:
        payments['payments_object'] = payments.apply(lambda row: Payments(
                                                                          payment_sequential=row['payment_sequential'],
                                                                          payment_type=row['payment_type'],
                                                                          payment_installments=row['payment_installments'],
                                                                          payment_value=row['payment_value'],
                                                                          order=OrderPlaced.objects.get(order_id=row['order_id'])), axis=1)
        payments_objects = payments['payments_object'].tolist()
        Payments.objects.bulk_create(payments_objects)

##
# Insert les reviews en bdd
#
def insertOrderReviews():
    reviews_directory = 'api/upload/olist_order_reviews_dataset_propre.csv'
    reviews = pd.read_csv(reviews_directory, encoding='unicode_escape')

    # Replace empty values with None
    reviews = reviews.replace('', np.nan).replace(np.nan, None)
   
    exist_reviews = pd.DataFrame(list(Reviews.objects.all().values()))

    order_placed = pd.DataFrame(list(OrderPlaced.objects.all().values('order_id')))
    reviews = reviews[reviews['order_id'].isin(order_placed['order_id'])]

    if not exist_reviews.empty:
       reviews = reviews[~reviews['review_id'].isin(exist_reviews['review_id'])]

    if not reviews.empty:
        reviews['reviews_object'] = reviews.apply(lambda row: Reviews(
                                                                    review_id=row['review_id'],
                                                                    review_score=row['review_score'],
                                                                    review_comment_title=row['review_comment_title'],
                                                                    review_comment_message=row['review_comment_message'],
                                                                    review_creation_date=row['review_creation_date'],
                                                                    review_answer_timestamp=row['review_answer_timestamp'],
                                                                    order=OrderPlaced.objects.get(order_id=row['order_id'])), axis=1)
        reviews_objects = reviews['reviews_object'].tolist()
        Reviews.objects.bulk_create(reviews_objects)