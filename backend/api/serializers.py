from rest_framework import serializers
from .models import Files ,Geolocation ,OrderItem

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product_id', 'quantity', 'total')


class GeolocationNormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocation
        fiels = ('state', 'quantity', 'total')