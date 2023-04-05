#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customers(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=50)
    customer_unique_id = models.CharField(max_length=50, blank=True, null=True)
    geolocation_zip_code_prefix = models.ForeignKey('GeolocationNorm', models.DO_NOTHING, db_column='geolocation_zip_code_prefix')

    class Meta:
        managed = False
        db_table = 'customers'


class Files(models.Model):
    id_file = models.AutoField(primary_key=True)
    file = models.CharField(max_length=50, blank=True, null=True)
    file_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'files'


class Geolocation(models.Model):
    id_geolocation = models.AutoField(primary_key=True)
    geolocation_zip_code_prefix = models.CharField(max_length=50, blank=True, null=True)
    geolocation_lat = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    geolocation_lng = models.DecimalField(max_digits=20, decimal_places=17, blank=True, null=True)
    geolocation_city = models.CharField(max_length=255, blank=True, null=True)
    geolocation_state = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geolocation'


class GeolocationNorm(models.Model):
    geolocation_zip_code_prefix = models.CharField(primary_key=True, max_length=50)
    geolocation_city = models.CharField(max_length=50, blank=True, null=True)
    geolocation_state = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geolocation_norm'


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('OrderPlaced', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    seller = models.ForeignKey('Sellers', models.DO_NOTHING, blank=True, null=True)
    shipping_limit_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    freight_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    order_item_quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_item'
        unique_together = (('order', 'product', 'seller'),)


class OrderPlaced(models.Model):
    order_id = models.CharField(primary_key=True, max_length=50)
    order_status = models.CharField(max_length=50, blank=True, null=True)
    order_purchase_timestamp = models.DateTimeField(blank=True, null=True)
    order_approved_at = models.DateTimeField(blank=True, null=True)
    order_delivered_carrier_date = models.DateTimeField(blank=True, null=True)
    order_delivered_customer_date = models.DateTimeField(blank=True, null=True)
    order_estimated_delivery_date = models.DateTimeField(blank=True, null=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_placed'


class Payments(models.Model):
    payments_id = models.CharField(primary_key=True, max_length=50)
    payment_sequential = models.IntegerField(blank=True, null=True)
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    payment_installments = models.IntegerField(blank=True, null=True)
    payment_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    order = models.ForeignKey(OrderPlaced, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'payments'


class Products(models.Model):
    product_id = models.CharField(primary_key=True, max_length=50)
    product_category_name = models.CharField(max_length=50, blank=True, null=True)
    product_height_cm = models.IntegerField(blank=True, null=True)
    product_width_cm = models.IntegerField(blank=True, null=True)
    product_name_lenght = models.IntegerField(blank=True, null=True)
    product_description_lenght = models.IntegerField(blank=True, null=True)
    product_photos_qty = models.IntegerField(blank=True, null=True)
    product_weight_g = models.IntegerField(blank=True, null=True)
    product_length_cm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Reviews(models.Model):
    review_id = models.CharField(primary_key=True, max_length=50)
    review_score = models.IntegerField(blank=True, null=True)
    review_comment_title = models.CharField(max_length=50, blank=True, null=True)
    review_comment_message = models.CharField(max_length=50, blank=True, null=True)
    review_creation_date = models.DateTimeField(blank=True, null=True)
    review_answer_timestamp = models.DateTimeField(blank=True, null=True)
    order = models.ForeignKey(OrderPlaced, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reviews'


class Sellers(models.Model):
    seller_id = models.CharField(primary_key=True, max_length=50)
    geolocation_zip_code_prefix = models.ForeignKey(GeolocationNorm, models.DO_NOTHING, db_column='geolocation_zip_code_prefix')

    class Meta:
        managed = False
        db_table = 'sellers'

