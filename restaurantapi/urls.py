from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('groups', views.GroupViewSet, basename='groups')
router.register('menu-items', views.MenuItemViewSet, basename='menu items')

urlpatterns = [
    path('', include(router.urls)),
    path('groups/manager/users', views.ManagerListCreateView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerDestroyView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewListCreateView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewDestroyView.as_view()),
    path('cart/menu-items', views.CartCreateListDeleteView.as_view()),
    path('orders', views.OrderListCreateView.as_view()),
    path('orders/<int:pk>', views.OrderRetrieveUpdateDeleteView.as_view()),
]