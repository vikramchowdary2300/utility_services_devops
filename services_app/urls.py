"""
URL configuration for utility_services project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include,path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    
    path('logout',views.logout.as_view(), name="logout"),
    path('about_us',views.about_us.as_view(), name="about_us"),
    #path('/',views.index, name = 'mytest'),
    path('',views.user_home.as_view(), name="home_page"),
    path('services/', views.services.as_view(), name='services'), 
    path('emergency_services/', views.emergency_services.as_view(), name='emergency_services'), 
    path('available_providers/', views.select_provider.as_view(), name='service_providers'),
    path('subscriptions/', views.subscription.as_view(), name='subscriptions'),
    path('add_to_cart/', views.add_to_cart.as_view(), name='add_to_cart'),
    path('payment/', views.payment.as_view(), name='payment'),
    path('confirm_payment/', views.confirm_payment.as_view(), name='confirm_payment'),
    path('orders/', views.orders.as_view(), name='orders'),
    path('user_subscriptions/', views.user_subscriptions.as_view(), name='user_subscriptions'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('login', views.login.as_view(), name='login'),

    
    #-------------------------  Service Provider ------------------------------
    path('sp_orders', views.sp_orders.as_view(), name='sp_orders'),
    path('sp_subscriptions', views.sp_subscriptions.as_view(), name='sp_subscriptions'),
    path('sp_services', views.sp_services.as_view(), name='sp_services'),
    path('sp_add_service', views.sp_add_service.as_view(), name='sp_add_service'),
    path('sp_order_details', views.sp_order_details.as_view(), name='sp_order_details'),
    path('fetch_services/', views.fetch_services.as_view(), name='fetch_services'),
    path('edit_service/<int:service_id>/', views.sp_add_service.as_view(), name='sp_edit_service'),
    
    
    
    #-------------------------  ADMIN ------------------------------
    path('dashboard', views.admin_dashboard.as_view(), name='admin_dashboard'),
    path('categories', views.admin_categories.as_view(), name='admin_categories'),
    path('services', views.admin_services.as_view(), name='admin_services'),
    path('service_providers', views.admin_service_providers.as_view(), name='admin_service_providers'),
    path('orders', views.admin_orders.as_view(), name='admin_orders'),
    path('customers', views.admin_customers.as_view(), name='admin_customers'),
    path('add_category', views.admin_add_category.as_view(), name='admin_add_category'),
    path('add_service', views.admin_add_service.as_view(), name='admin_add_service'),
    path('edit_services/<int:service_id>/', views.admin_add_service.as_view(), name='admin_edit_services'),
    path('edit_category/<int:category_id>/', views.admin_add_category.as_view(), name='admin_edit_category'),
    path('admin_sp_services', views.admin_sp_services.as_view(), name='admin_sp_services'),
    path('admin_order_details', views.admin_order_details.as_view(), name='admin_order_details'),
    path('subscriptions', views.admin_subscriptions.as_view(), name='admin_subscriptions'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



