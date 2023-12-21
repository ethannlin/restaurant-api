from django.shortcuts import render
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, status
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager, IsDeliveryCrew, IsCustomer, IsManagerOrDeliveryCrew, IsManagerOrCustomer
from django.db import transaction

# Create your views here.
'''
    Group views
'''
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filterset_fields = ['name']
    ordering_fields = ['name']
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'status': 'group created'}
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'status': 'group updated'}
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        response.data = {'status': 'group updated'}
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'status': 'group deleted'}, status=status.HTTP_200_OK)
    
'''
    User views
'''
class ManagerListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, IsManager]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in self.permission_classes]
        
    def post(self, request, *args, **kwargs):
        username = request.data['username']

        try:
            user = User.objects.get(username=username)
            manager_group = Group.objects.get(name='manager')
            user.groups.add(manager_group)
            return Response({'status': 'user added to the manager group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ManagerDestroyView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
            manager_group = Group.objects.get(name='manager')
            user.groups.remove(manager_group)
            return Response({'status': 'user removed from the manager group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
'''
    Delivery Crew views
'''
class DeliveryCrewListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='delivery crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
        
    def post(self, request, *args, **kwargs):
        username = request.data['username']

        try:
            user = User.objects.get(username=username)
            delivery_crew_group = Group.objects.get(name='delivery crew')
            user.groups.add(delivery_crew_group)
            return Response({'status': 'user added to the delivery crew group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class DeliveryCrewDestroyView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='delivery crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
            delivery_crew_group = Group.objects.get(name='delivery crew')
            user.groups.remove(delivery_crew_group)
            return Response({'status': 'user removed from the delivery crew group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

'''
    Category views
'''
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['title']
    ordering_fields = ['title']
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsManager]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'status': 'category created'}
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'status': 'category updated'}
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        response.data = {'status': 'category updated'}
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'status': 'category deleted'}, status=status.HTTP_200_OK)
    
'''
    Menu Item views
'''
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ['price', 'title', 'category']
    ordering_fields = ['price', 'title', 'category']
    search_fields = ['title', 'category']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsManager]
        return [permission() for permission in self.permission_classes]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'status': 'menu item created'}
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'status': 'menu item updated'}
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        response.data = {'status': 'menu item updated'}
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'status': 'menu item deleted'}, status=status.HTTP_200_OK)

'''
    Cart views
'''
class CartCreateListDeleteView(mixins.ListModelMixin, 
                                   mixins.CreateModelMixin, 
                                   mixins.DestroyModelMixin, 
                                   generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    filterset_fields = ['user', 'price', 'menuitem', 'quantity']
    ordering_fields = ['user', 'price', 'menuitem', 'quantity']

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        response.data = {'status': 'item added to cart'}
        return response
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    def delete(self, request, *args, **kwargs):
        Cart.objects.filter(user=self.request.user).delete()
        return Response({'status': 'cart cleared'}, status=status.HTTP_200_OK)

'''
    Order views
'''
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    filterset_fields = ['status', 'total', 'date']
    ordering_fields = ['status', 'total', 'date']

    def get_queryset(self):
        user = self.request.user
        if IsManager.has_permission(self, self.request, self):
            return Order.objects.all()
        elif IsDeliveryCrew.has_permission(self, self.request, self):
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=self.request.user)
        
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsCustomer]
        return [permission() for permission in self.permission_classes]
    
    def post(self, request, *args, **kwargs):
        if IsCustomer.has_permission(self, self.request, self):
            with transaction.atomic():
                if Cart.objects.filter(user=self.request.user).count() == 0:
                    return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(data={
                    "delivery_crew_id": None,
                    "status": False
                })
                serializer.is_valid(raise_exception=True)
                order = serializer.save(user=self.request.user)

                order_items = [OrderItem(order=order, menuitem=item.menuitem, quantity=item.quantity, unit_price=item.unit_price, price=item.price) for item in Cart.objects.filter(user=self.request.user)]
                OrderItem.objects.bulk_create(order_items)
                Cart.objects.filter(user=self.request.user).delete()
                return Response({'status': 'order created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Only customers can create orders'}, status=status.HTTP_401_UNAUTHORIZED)
        
class OrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    filterset_fields = ['status', 'total', 'date']
    ordering_fields = ['status', 'total', 'date']

    def get_queryset(self):
        user = self.request.user
        if IsManager.has_permission(self, self.request, self):
            return Order.objects.all()
        elif IsDeliveryCrew.has_permission(self, self.request, self):
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=self.request.user)
        
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, IsManagerOrCustomer]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsManager]
        elif self.request.method == 'PATCH':
            self.permission_classes = [IsManagerOrDeliveryCrew]
        return [permission() for permission in self.permission_classes]
    
    def put(self, request, *args, **kwargs):
        if IsManager.has_permission(self, self.request, self):
            response = self.update(request, *args, **kwargs)
            response.data = {"message": "Order updated successfully."}
            return response
        else:
            return Response({'error': 'Only managers can update orders'}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        if IsDeliveryCrew.has_permission(self, self.request, self) and not IsManager.has_permission(self, self.request, self):
            if list(request.data.keys()) == ['status']:
                response = self.partial_update(request, *args, **kwargs)
                response.data = {"message": "Order status updated successfully."}
                return response
            else:
                return Response({"error": "You can only update the specific attribute."}, status=status.HTTP_403_FORBIDDEN)
        response = self.partial_update(request, *args, **kwargs)
        response.data = {"message": "Order updated successfully."}
        return response
    
    def delete(self, request, *args, **kwargs):
        if IsManager.has_permission(self, self.request, self):
            response = self.destroy(request, *args, **kwargs)
            return Response({"message": "Order deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only managers can delete orders'}, status=status.HTTP_403_FORBIDDEN)
    
    
