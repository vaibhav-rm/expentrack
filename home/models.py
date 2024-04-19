from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class History(models.Model):
    desc = models.CharField(max_length=20)
    amount = models.IntegerField()

class Balance(models.Model):
    balance = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    expense = models.IntegerField(default=0)

@receiver(post_save, sender=History)
def update_balance(sender, instance, created, **kwargs):
    history = instance
    if created:  # Only update balance on new History instances
        balance, _ = Balance.objects.get_or_create(id=1)  # Assuming there's only one Balance object
        balance.balance += history.amount
        if history.amount > 0:
            balance.income += history.amount
        elif history.amount < 0:
            balance.expense += history.amount
        balance.save()
