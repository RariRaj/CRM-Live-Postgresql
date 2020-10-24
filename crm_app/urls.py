from django.urls import path
from crm_app import views

#authentication views of django for reset password
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('',views.home,name="home"),
    path('products',views.products,name="products"),
    path('customer/<str:id>',views.customer,name="customer"),
    path('create_order/<str:id>',views.createOrder,name="create_order"),
    path('update_order/<str:id>',views.updateOrder,name="update_order"),
    path('delete_order/<str:id>',views.deleteOrder,name="delete_order"),
    path('update_customer/<str:id>',views.updateCustomer,name="update_customer"),
    path('create_customer',views.createCustomer,name="create_customer"),
    path('registration',views.registration,name="registration"),
    path('loginuser',views.loginPage,name="loginuser"),
    path('logoutuser',views.logoutUser,name="logoutuser"),
    path('userhome',views.userHome,name="userhome"),
    path('settings',views.userSettings,name="settings"),

    #auth views

    #Submit email form
    path('password_reset/', auth_views.PasswordResetView.as_view(),name="password_reset"),

    #Email sent success message
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),

    #Link to password reset form in email
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),

    #Password changed successfully message
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),


]
