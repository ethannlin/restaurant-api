from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem_id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    delivery_crew_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    status = serializers.BooleanField(required=False)
    date = serializers.DateField(read_only=True)
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date', 'order_items']