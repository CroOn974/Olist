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
    state_name = serializers.CharField()
    data = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = ['state_name', 'data']


class EvoProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    data = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = ['product', 'data']


class TurnoverYearSerializer(serializers.ModelSerializer):
    year = serializers.CharField()
    turnover = serializers.IntegerField()
    turnover_percentage = serializers.IntegerField()
    avg_basket = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['year', 'turnover', 'turnover_percentage', 'avg_basket']


class NewCustomerSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['quantity']


class InterVsExterSerializer(serializers.ModelSerializer):
    inter_region = serializers.IntegerField()
    exter_region = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['inter_region','exter_region']
