from rest_framework import serializers
from .models import Files,OrderItem,State,Products

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


class SoldProductSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    turnover = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Products
        fields = ['product_id', 'turnover', 'quantity']

class CaStateSerializer(serializers.Serializer):
    state_name = serializers.CharField()
    turnover = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = State
        fields = ['state_name', 'turnover', 'quantity']


class EvoStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fiels = ('state', 'quantity', 'turnover', 'year')


class EvoProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fiels = ('product_id', 'quantity', 'turnover', 'year')