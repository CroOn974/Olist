from rest_framework import serializers
from .models import Files ,Geolocation ,OrderItem

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


class SoldProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product_id', 'quantity', 'total')


class CaStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fiels = ('state', 'quantity', 'total')


class EvoStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fiels = ('state', 'ca', 'year')
