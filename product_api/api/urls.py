from django.urls import path
from . import views
from message_service import views as sms_views
from django.urls import include, path

 # api app urls
urlpatterns = [
    path('', views.home, name='api-home'),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('sms/', sms_views.sms_response),
    path('rest-auth/', include('rest_auth.urls')),

]
