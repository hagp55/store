from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Customer, Product

User = get_user_model()


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def update_customer(sender, instance, created, **kwargs):
    if created is False:
        instance.customer.save()


@receiver(pre_delete, sender=Product)
def myfield_delete(sender, instance, **kwargs):
    if instance.image.name:
        instance.image.delete(False)
