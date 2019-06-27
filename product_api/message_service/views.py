from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from api.models import Product
from api.views import ProductDetail
import re
from message_service.browser_automations import add_to_cart, checkout, add_and_checkout
from message_service.browser_settings import shipping, billing, card
from rest_framework.decorators import api_view, authentication_classes
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.
@csrf_exempt
@api_view(['POST'])
#@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def sms_response(request):
    body = request.POST.get('Body', '')
    print(body)
    if re.match(r'^query\s\d+', body, re.IGNORECASE) is not None:
        r = get_product_details(body)
        return HttpResponse(r.to_xml(), content_type='text/xml')
    elif re.match(r'^query\sall', body, re.IGNORECASE):
        r = MessagingResponse()
        products = ProductDetail.queryset.values_list('id', 'name', 'price', 'url')
        r.message(str([i for i in products]))
        return HttpResponse(r.to_xml(), content_type='text/xml')
    elif re.match(r'^buy\s\d', body, re.IGNORECASE):
        id = re.findall(r'\d.*', body, re.IGNORECASE)[0]
        product = ProductDetail.queryset.filter(id=id)[0]
        print(Product.url)
        add_and_checkout(product.url)

def get_product_details(body):
    r = MessagingResponse()
    id = re.findall(r'\d.*', body, re.IGNORECASE)[0]
    print(f'id number id {id}')
    try:
        product = ProductDetail.queryset.filter(id=id)[0]
        r.message(f"Name: {product}, Price: {product.price}, In stock: {product.stock}, Url: {product.url}")
    except IndexError:
        r.message('Product not found!')
    return r
    