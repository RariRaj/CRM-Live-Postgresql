from django.urls import path
from crm_app import views

urlpatterns = [
    
    path('',views.home,name="home"),
    path('products',views.products,name="products"),
    path('customer/<str:id>',views.customer,name="customer"),
    path('create_order/<str:id>',views.createOrder,name="create_order"),
    path('update_order/<str:id>',views.updateOrder,name="update_order"),
    path('delete_order/<str:id>',views.deleteOrder,name="delete_order"),
    path('update_customer/<str:id>',views.updateCustomer,name="update_customer"),
    path('create_customer',views.createCustomer,name="create_customer"),

]
