from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
    
# Create your models here.
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    desc = models.CharField(max_length=20)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    balance = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    expense = models.IntegerField(default=0)

@receiver(post_save, sender=History)
def update_balance(sender, instance, created, **kwargs):
    history = instance
    if created: 
        balance, _ = Balance.objects.get_or_create(id=1) 
        balance.balance += history.amount
        if history.amount > 0:
            balance.income += history.amount
        elif history.amount < 0:
            balance.expense += history.amount
        balance.save()
