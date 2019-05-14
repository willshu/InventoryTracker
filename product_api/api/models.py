from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from twilio.rest import Client

class Product(models.Model):
    name = models.TextField()
    price = models.TextField()
    url = models.TextField()
    stock = models.BooleanField(default=False)
    #pk "Product Key" is an automatically generated 

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = True if self.pk is None else False
        if is_new is True and self.stock is True:
            super(Product, self).save(*args, **kwargs)
            self.send_sms()
        elif is_new is True and self.stock is False:
            super(Product, self).save(*args, **kwargs)
            pass
        else:
            old = Product.objects.get(pk=self.pk)
            if old.stock is False and self.stock is True:
                self.send_sms()
            super(Product, self).save(*args, **kwargs)

    # def _eq(self, other):
    #     if hash((self.name, self.price, self.url, self.stock)) == hash((other.name, other.price, other.url, other.stock)):
    #         return True
    #     else:
    #         return False

    # def _is_new_or_changed(self, new=False):
    #     if self.stock == True or new is True:
    #         return True

    def send_sms(self):
        account_sid = 'AC96f6f4da9705c753c6e1a683804a6484'
        auth_token = 'e7f8e2645407634ebd29d05edea180d8'
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                    body="New item {} product ID {} price {}".format(self.name, self.pk, self.price),
                    from_='+16467982219',
                    to='+19177103981'
                )
        print(message)
    
